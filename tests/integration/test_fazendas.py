import pytest
from fastapi.testclient import TestClient

from brain_app.main import app
from tests.utils.payloads import fazenda_payload, produtor_payload

client = TestClient(app)


class TestFazendasIntegration:
    @pytest.mark.order(7)
    def test_criar_produtor(self, client):
        produtor_data = produtor_payload()
        response = client.post("/produtores/", json=produtor_data)
        pytest.produtor_cpf_cnpj = response.json()["cpf_cnpj"]
        pytest.produtor_id = response.json()["id"]
        assert response.status_code == 201

    @pytest.mark.order(8)
    def test_criar_fazenda(self, client):
        fazenda_data = fazenda_payload(pytest.produtor_id)
        response = client.post("/fazendas/", json=fazenda_data)
        fazenda = response.json()
        pytest.fazenda_id = fazenda["id"]
        assert response.status_code == 201
        assert fazenda["nome_fazenda"] == fazenda_data["nome_fazenda"]

    @pytest.mark.order(9)
    def test_buscar_fazenda_por_id(self, client):
        response = client.get(f"/fazendas/{pytest.fazenda_id}")
        assert response.status_code == 200
        assert response.json()["id"] == pytest.fazenda_id

    @pytest.mark.order(10)
    def test_atualizar_fazenda(self, client):
        update_data = {"nome_fazenda": "Fazenda Atualizada"}
        response = client.put(f"/fazendas/{pytest.fazenda_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["nome_fazenda"] == "Fazenda Atualizada"

    @pytest.mark.order(11)
    def test_deletar_fazenda(self, client):
        response = client.delete(f"/fazendas/{pytest.fazenda_id}")
        produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
        response = client.delete(f"/produtores/{produtor_cpf_cnpj}")
        assert response.status_code == 204
        assert response.status_code == 204

    @pytest.mark.order(12)
    def test_buscar_fazenda_apos_delete(self, client):
        response = client.get(f"/fazendas/{pytest.fazenda_id}")
        assert response.status_code == 404
