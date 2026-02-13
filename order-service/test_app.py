import os
os.environ["DB_NAME"] = "test"
os.environ["DB_USER"] = "test"
os.environ["DB_PASSWORD"] = "test"
os.environ["DB_HOST"] = "localhost"
from app import app

def test_metrics_route():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"orders_created_total" in response.data
    assert response.status_code == 200
    assert b"orders_created_total" in response.data
