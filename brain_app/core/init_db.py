from sqlalchemy import text

from brain_app.core.database import engine
from brain_app.models import models


def create_schema(schema_name: str):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        conn.commit()


def init_db():
    schema = "brain_app"
    create_schema(schema)
    models.Base.metadata.create_all(bind=engine)
