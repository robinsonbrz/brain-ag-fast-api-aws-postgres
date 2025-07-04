from sqlalchemy.orm import Session

from brain_app.core.database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
