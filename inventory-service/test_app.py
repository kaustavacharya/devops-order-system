import os
# When running inside the compose environment tests should use the service hostnames
os.environ["REDIS_HOST"] = os.environ.get("REDIS_HOST", "inventory-db")
os.environ["REDIS_PORT"] = os.environ.get("REDIS_PORT", "6379")
os.environ["BROKER_HOST"] = os.environ.get("BROKER_HOST", "rabbitmq")
os.environ["BROKER_PORT"] = os.environ.get("BROKER_PORT", "5672")
from app import app

def test_metrics_route():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"orders_processed_total" in response.data
