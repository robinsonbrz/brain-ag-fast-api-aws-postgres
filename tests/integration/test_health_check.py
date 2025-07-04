from fastapi.testclient import TestClient

from brain_app.main import app

client = TestClient(app)


class TestHealthCheckIntegration:
    def test_health_check(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "Healthy!"}
