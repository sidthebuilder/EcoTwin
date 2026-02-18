from fastapi.testclient import TestClient
from app.main import app
from app.api.health import health_check

client = TestClient(app)

def test_health_check_endpoint():
    """
    Verifies that the health check endpoint returns 200/503 structure correctly.
    Note: Can return 503 if dependencies aren't mocked, which is expected here.
    """
    response = client.get("/api/v1/health")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert "components" in data

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_metrics_endpoint():
    """Verify Prometheus metrics are exposed"""
    response = client.get("/metrics")
    assert response.status_code == 200
