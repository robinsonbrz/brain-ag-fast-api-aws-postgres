import pytest
from fastapi.testclient import TestClient
from brain_app.main import app
from sqlalchemy.orm import Session
from pprint import pprint

client = TestClient(app)

@pytest.mark.order(13)
def test_list_culturas_vazia(client, db_session):
    response = client.get("/culturas/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.order(14)
def test_criar_produtor(client):
    produtor_data = {"cpf_cnpj": "690.692.120-72", "nome_produtor": "Produtor Teste cpf fake"}
    response = client.post("/produtores/", json=produtor_data)
    pprint(response.json())
    assert response.status_code == 201
    pytest.produtor_cpf_cnpj = response.json()["cpf_cnpj"]
    pytest.produtor_id = response.json()["id"]

@pytest.mark.order(15)
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


@pytest.mark.order(16)
def test_create_cultura(client):
    cultura_data = {
        "fazenda_id": pytest.fazenda_id,
        "nome_cultura": "Manga",
        "ano_safra": 2025,
        "area_plantada": 40.0
    }
    response = client.post("/culturas/", json=cultura_data)
    cultura = response.json()
    pytest.cultura_id = cultura["id"]
    assert response.status_code == 201
    assert response.json()["nome_cultura"] == cultura_data["nome_cultura"]

@pytest.mark.order(17)
def test_get_cultura(client):
    cultura_id = pytest.cultura_id
    res = client.get(f"/culturas/{cultura_id}")
    assert res.status_code == 200
    assert res.json()["id"] == cultura_id

@pytest.mark.order(18)
def test_update_cultura(client):
    cultura_id = pytest.cultura_id
    cultura_data = {
        "fazenda_id": cultura_id,
        "nome_cultura": "Manga",
        "ano_safra": 2025,
        "area_plantada": 40.0
    }
    cultura_data["nome_cultura"]=  "Milho"
    res = client.put(f"/culturas/{cultura_id}", json=cultura_data)
    assert res.status_code == 200
    assert res.json()["nome_cultura"] == "Milho"

@pytest.mark.order(20)
def test_delete_cultura(client):
    cultura_id = pytest.cultura_id
    res = client.delete(f"/culturas/{cultura_id}")
    assert res.status_code == 204

@pytest.mark.order(21)
def test_deletar_fazenda(client):
    response = client.delete(f"/fazendas/{pytest.fazenda_id}")
    assert response.status_code == 204
    produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
    response = client.delete(f"/produtores/{produtor_cpf_cnpj}")
    assert response.status_code == 204

@pytest.mark.order(22)
def test_get_cultura_after_delete(client):
    cultura_id = pytest.cultura_id
    res = client.get(f"/culturas/{cultura_id}")
    assert res.status_code == 404
