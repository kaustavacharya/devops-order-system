# flask: Web framework for HTTP endpoints
# redis: Redis database client
# pika: RabbitMQ client library
# os: Access environment variables
# json: Parse message bodies

from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
processed_counter = Counter('orders_processed_total', 'Orders processed from RabbitMQ')
import redis
import pika
import os
import json

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "inventory-db"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    decode_responses=True
)


# Connect to RabbitMQ with retry logic
import time
max_retries = 10
for attempt in range(max_retries):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.environ.get("BROKER_HOST", "rabbitmq"),
                port=int(os.environ.get("BROKER_PORT", 5672))
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='order_created')
        break
    except pika.exceptions.AMQPConnectionError:
        wait = 2 * (attempt + 1)
        print(f"[inventory-service] RabbitMQ not ready, retrying in {wait}s...")
        time.sleep(wait)
else:
    raise RuntimeError("[inventory-service] Could not connect to RabbitMQ after retries.")

# Callback to handle incoming messages

def callback(ch, method, properties, body):
    order = json.loads(body)
    item = order["item"]
    quantity = int(order["quantity"])

    # Increment Prometheus counter
    processed_counter.inc()

    # Update Redis inventory
    current = r.get(item)
    if current is None:
        r.set(item, 100 - quantity)  # assume default stock = 100
    else:
        r.set(item, int(current) - quantity)
    print(f"Processed order: {order}, remaining stock: {r.get(item)}")
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

channel.basic_consume(
    queue='order_created',
    on_message_callback=callback,
    auto_ack=True
)

@app.route("/inventory/<item>", methods=["GET"])
def get_inventory(item):
    stock = r.get(item)
    if stock is None:
        return jsonify({"item": item, "stock": 0})
    return jsonify({"item": item, "stock": int(stock)})

import threading

def run_flask():
    app.run(host="0.0.0.0", port=5001)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    print("Waiting for orders...")
    channel.start_consuming()
