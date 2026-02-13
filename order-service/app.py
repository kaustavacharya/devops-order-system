
# Flask: Web framework for REST APIs
# psycopg2: PostgreSQL database driver
# pika: RabbitMQ client library
# os: Access environment variables

from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import psycopg2
import pika
import os
import json

app = Flask(__name__)
order_counter = Counter('orders_created_total', 'Total number of orders created')

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

def get_db_connection():
    db_url = os.environ.get("DB_URL")
    if db_url:
        return psycopg2.connect(db_url)
    # fallback for local/dev, now requires env vars (no hardcoded defaults)
    return psycopg2.connect(
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", 5432)
    )

def ensure_orders_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        item VARCHAR(255) NOT NULL,
        quantity INT NOT NULL
    )
    """
    )
    conn.commit()
    cursor.close()

def get_rabbitmq_channel():
    import time
    max_retries = 10
    broker_url = os.environ.get("BROKER_URL")
    for attempt in range(max_retries):
        try:
            if broker_url:
                rabbit_conn = pika.BlockingConnection(pika.URLParameters(broker_url))
            else:
                rabbit_conn = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=os.environ.get("BROKER_HOST", "rabbitmq"),
                        port=int(os.environ.get("BROKER_PORT", 5672))
                    )
                )
            channel = rabbit_conn.channel()
            channel.queue_declare(queue='order_created')
            return channel
        except pika.exceptions.AMQPConnectionError:
            wait = 2 * (attempt + 1)
            print(f"[order-service] RabbitMQ not ready, retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("[order-service] Could not connect to RabbitMQ after retries.")

# Initialize connections
conn = get_db_connection()
ensure_orders_table(conn)


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    cursor = conn.cursor()
    # Accept both 'item_id' and 'item' for compatibility
    item = data.get("item_id") or data.get("item")
    quantity = data["quantity"]
    cursor.execute(
        "INSERT INTO orders (item, quantity) VALUES (%s, %s) RETURNING id",
        (item, quantity)
    )
    order_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()

    # Increment Prometheus counter
    order_counter.inc()

    # Create RabbitMQ channel for each request
    channel = get_rabbitmq_channel()
    # Publish event to RabbitMQ as valid JSON
    event = {"id": order_id, "item": item, "quantity": quantity}
    channel.basic_publish(
        exchange='',
        routing_key='order_created',
        body=json.dumps(event)
    )
    channel.close()
    return jsonify({"id": order_id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
