from pprint import pprint

import pytest
from fastapi.testclient import TestClient

from brain_app.main import app

client = TestClient(app)


class TestDashboardIntegration:
    @pytest.mark.order(19)
    def test_dashboard(self, client):
        response = client.get("/dashboard")
        assert response.status_code == 200
        data = response.json()
        pprint(data)
        assert "total_fazendas_cadastradas" in data
        assert "total_area_registrada" in data
        assert "fazendas_por_estado" in data
        assert "culturas_plantadas" in data
        assert "uso_solo" in data
