from pprint import pprint
import pytest
from fastapi.testclient import TestClient
from brain_app.main import app

client = TestClient(app)

@pytest.mark.order(6)
def test_list_fazendas_vazia(client, db_session):
    response = client.get("/fazendas/")
    pprint(response.json())
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.order(7)
def test_criar_produtor(client):
    produtor_data = {"cpf_cnpj": "690.692.120-72", "nome_produtor": "Produtor Teste cpf fake"}
    response = client.post("/produtores/", json=produtor_data)
    pprint(response.json())
    assert response.status_code == 201
    pytest.produtor_cpf_cnpj = response.json()["cpf_cnpj"]
    pytest.produtor_id = response.json()["id"]

@pytest.mark.order(8)
def test_criar_fazenda(client):
    fazenda_data = {
        "produtor_id": pytest.produtor_id,
        "nome_fazenda": "Fazenda Teste",
        "cidade": "Cidade Teste",
        "estado": "ST",
        "area_total": 100.0,
        "area_agricultavel": 50.0,
        "area_vegetacao": 40.0
    }
    response = client.post("/fazendas/", json=fazenda_data)
    assert response.status_code == 201
    fazenda = response.json()
    pytest.fazenda_id = fazenda["id"]
    assert fazenda["nome_fazenda"] == "Fazenda Teste"

@pytest.mark.order(9)
def test_buscar_fazenda_por_id(client):
    response = client.get(f"/fazendas/{pytest.fazenda_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pytest.fazenda_id

@pytest.mark.order(10)
def test_atualizar_fazenda(client):
    update_data = {"nome_fazenda": "Fazenda Atualizada"}
    response = client.put(f"/fazendas/{pytest.fazenda_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nome_fazenda"] == "Fazenda Atualizada"

@pytest.mark.order(11)
def test_deletar_fazenda(client):
    response = client.delete(f"/fazendas/{pytest.fazenda_id}")
    assert response.status_code == 204
    produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
    response = client.delete(f"/produtores/{produtor_cpf_cnpj}")
    assert response.status_code == 204

@pytest.mark.order(12)
def test_buscar_fazenda_apos_delete(client):
    response = client.get(f"/fazendas/{pytest.fazenda_id}")
    assert response.status_code == 404
