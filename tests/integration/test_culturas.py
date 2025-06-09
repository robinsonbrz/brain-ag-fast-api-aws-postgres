from pprint import pprint

import pytest
from fastapi.testclient import TestClient

from brain_app.main import app
from tests.utils.payloads import cultura_payload, fazenda_payload, produtor_payload

client = TestClient(app)


class TestCulturasIntegration:
    @pytest.mark.order(13)
    def test_list_culturas_vazia(self, client):
        response = client.get("/culturas/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.order(14)
    def test_criar_produtor(self, client):
        produtor_data = produtor_payload()
        response = client.post("/produtores/", json=produtor_data)
        pprint(response.json())
        pytest.produtor_cpf_cnpj = response.json()["cpf_cnpj"]
        pytest.produtor_id = response.json()["id"]
        assert response.status_code == 201

    @pytest.mark.order(15)
    def test_criar_fazenda(self, client):
        fazenda_data = fazenda_payload(pytest.produtor_id)
        response = client.post("/fazendas/", json=fazenda_data)
        fazenda = response.json()
        pytest.fazenda_id = fazenda["id"]
        assert response.status_code == 201
        assert fazenda["nome_fazenda"] == fazenda_data["nome_fazenda"]

    @pytest.mark.order(16)
    def test_create_cultura(self, client):
        cultura_data = cultura_payload(pytest.fazenda_id)
        response = client.post("/culturas/", json=cultura_data)
        cultura = response.json()
        pytest.cultura_id = cultura["id"]
        assert response.status_code == 201
        assert cultura["nome_cultura"] == cultura_data["nome_cultura"]

    @pytest.mark.order(17)
    def test_get_cultura(self, client):
        cultura_id = pytest.cultura_id
        res = client.get(f"/culturas/{cultura_id}")
        assert res.status_code == 200
        assert res.json()["id"] == cultura_id

    @pytest.mark.order(18)
    def test_update_cultura(self, client):
        cultura_id = pytest.cultura_id
        cultura_data = cultura_payload(cultura_id)
        cultura_data["nome_cultura"] = "Milho"
        res = client.put(f"/culturas/{cultura_id}", json=cultura_data)
        assert res.status_code == 200
        assert res.json()["nome_cultura"] == "Milho"

    @pytest.mark.order(20)
    def test_delete_cultura(self, client):
        cultura_id = pytest.cultura_id
        res = client.delete(f"/culturas/{cultura_id}")
        assert res.status_code == 204

    @pytest.mark.order(21)
    def test_deletar_fazenda(self, client):
        response = client.delete(f"/fazendas/{pytest.fazenda_id}")
        assert response.status_code == 204
        produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
        response = client.delete(f"/produtores/{produtor_cpf_cnpj}")
        assert response.status_code == 204

    @pytest.mark.order(30)
    def test_get_cultura_after_delete(self, client):
        cultura_id = pytest.cultura_id
        res = client.get(f"/culturas/{cultura_id}")
        pprint(res.json())
        assert res.status_code == 404
