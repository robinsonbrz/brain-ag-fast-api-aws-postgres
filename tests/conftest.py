import pytest
from fastapi.testclient import TestClient

from brain_app.core import init_db
from brain_app.core.database import SessionLocal
from brain_app.main import app
from brain_app.models.models import Fazenda, Produtor
from tests.utils.payloads import fazenda_payload, produtor_payload


@pytest.fixture(scope="function")
def db_session():
    init_db.init_db()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture
def produtor(db_session) -> Produtor:
    produtor = Produtor(**produtor_payload())
    db_session.add(produtor)
    db_session.commit()
    return produtor


@pytest.fixture
def fazenda(db_session, produtor: Produtor) -> Fazenda:
    fazenda = Fazenda(**fazenda_payload(produtor.id))
    db_session.add(fazenda)
    db_session.commit()
    return fazenda
