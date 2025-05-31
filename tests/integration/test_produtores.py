import pytest
from fastapi.testclient import TestClient
from brain_app.main import app
from brain_app.core.database import SessionLocal, Base, engine
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    # Criar todas as tabelas antes do teste
    #Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    # Dropar tabelas após testes (limpeza)
    # Base.metadata.drop_all(bind=engine)

def test_crud_produtor(db_session: Session):
    # POST criar produtor válido
    produtor_data = {"cpf_cnpj": "12345678901", "nome_produtor": "João Silva"}
    response = client.post("/produtores/", json=produtor_data)
    assert response.status_code == 201
    produtor = response.json()
    assert produtor["cpf_cnpj"] == produtor_data["cpf_cnpj"]
    assert produtor["nome_produtor"] == produtor_data["nome_produtor"]
    produtor_id = produtor["id"]

    # GET por id
    response = client.get(f"/produtores/{produtor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == produtor_id

    # PUT atualizar nome
    update_data = {"nome_produtor": "João Atualizado"}
    response = client.put(f"/produtores/{produtor_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nome_produtor"] == "João Atualizado"

    # DELETE
    response = client.delete(f"/produtores/{produtor_id}")
    assert response.status_code == 204

    # GET após delete deve retornar 404
    response = client.get(f"/produtores/{produtor_id}")
    assert response.status_code == 404
