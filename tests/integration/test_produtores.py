from pprint import pprint

import pytest

from brain_app.utils.validators import limpar_mascara


@pytest.mark.order(1)
def test_post_produtor_valido(client, db_session):
    produtor_data = {"cpf_cnpj": "690.692.120-72", "nome_produtor": "Produtor Teste cpf fake"}
    response = client.post("/produtores/", json=produtor_data)
    pprint(response.json())
    assert response.status_code == 201
    produtor = response.json()

    pytest.produtor_cpf_cnpj = response.json()["cpf_cnpj"]
    assert produtor["cpf_cnpj"] == limpar_mascara(produtor_data["cpf_cnpj"])
    assert produtor["nome_produtor"] == produtor_data["nome_produtor"]


@pytest.mark.order(2)
def test_get_produtor_por_cpf_cnpj(client):
    produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
    response = client.get(f"/produtores/{produtor_cpf_cnpj}")
    assert response.status_code == 200
    assert response.json()["cpf_cnpj"] == produtor_cpf_cnpj


@pytest.mark.order(3)
def test_put_atualizar_nome_produtor(client):
    produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
    update_data = {"nome_produtor": "João Atualizado"}
    response = client.put(f"/produtores/{produtor_cpf_cnpj}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nome_produtor"] == "João Atualizado"


@pytest.mark.order(4)
def test_delete_produtor(client):
    produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
    response = client.delete(f"/produtores/{produtor_cpf_cnpj}")
    assert response.status_code == 204


@pytest.mark.order(5)
def test_get_produtor_apos_delete(client):
    produtor_cpf_cnpj = pytest.produtor_cpf_cnpj
    response = client.get(f"/produtores/{produtor_cpf_cnpj}")
    assert response.status_code == 404
