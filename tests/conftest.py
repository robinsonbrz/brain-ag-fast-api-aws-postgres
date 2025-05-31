import os
# definidas antes de qualquer utilização
os.environ["DATABASE_URL"] = "postgresql://postgres:password@db:5432/postgres"
os.environ["POSTGRES_PASSWORD"] = "password"

import pytest
from fastapi.testclient import TestClient
from brain_app.main import app
from brain_app.core.database import SessionLocal, Base, engine
from brain_app.core import init_db


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
