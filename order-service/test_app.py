import pytest
from app import app

def test_metrics_route():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"orders_created_total" in response.data
