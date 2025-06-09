import pytest
from fastapi.testclient import TestClient

from brain_app.main import app
from brain_app.utils.validators import limpar_mascara
from tests.utils.payloads import produtor_payload

client = TestClient(app)


class TestProdutoresIntegration:
    @pytest.mark.order(1)
    def test_post_produtor_valido(self, client):
        produtor_data = produtor_payload()
        response = client.post("/produtores/", json=produtor_data)
        produtor = response.json()

        pytest.produtor_cpf_cnpj = response.json()["cpf_cnpj"]
        assert response.status_code == 201
        assert produtor["cpf_cnpj"] == limpar_mascara(produtor_data["cpf_cnpj"])
        assert produtor["nome_produtor"] == produtor_data["nome_produtor"]

    @pytest.mark.order(2)
    def test_get_produtor_por_cpf_cnpj(self, client):
        produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
        response = client.get(f"/produtores/{produtor_cpf_cnpj}")
        assert response.status_code == 200
        assert response.json()["cpf_cnpj"] == produtor_cpf_cnpj

    @pytest.mark.order(3)
    def test_put_atualizar_nome_produtor(self, client):
        produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
        update_data = {"nome_produtor": "João Atualizado"}
        response = client.put(f"/produtores/{produtor_cpf_cnpj}", json=update_data)
        assert response.status_code == 200
        assert response.json()["nome_produtor"] == "João Atualizado"

    @pytest.mark.order(4)
    def test_delete_produtor(self, client):
        produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
        response = client.delete(f"/produtores/{produtor_cpf_cnpj}")
        assert response.status_code == 204

    @pytest.mark.order(5)
    def test_get_produtor_apos_delete(self, client):
        produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
        response = client.get(f"/produtores/{produtor_cpf_cnpj}")
        assert response.status_code == 404
