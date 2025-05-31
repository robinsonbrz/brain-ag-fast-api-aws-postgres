import pytest
from fastapi.testclient import TestClient
from brain_app.main import app
from brain_app.core.database import SessionLocal, Base, engine

@pytest.fixture(scope="function")
def db_session():
    try:
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client():
    return TestClient(app) 
