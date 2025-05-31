from brain_app.core.database import engine
from brain_app.models import models

def init_db():
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Tabelas criadas com sucesso.")
