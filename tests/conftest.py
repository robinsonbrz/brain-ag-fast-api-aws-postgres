import pytest
from fastapi.testclient import TestClient

from brain_app.core import init_db
from brain_app.core.database import SessionLocal
from brain_app.main import app


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
