from sqlalchemy.orm import Session
from brain_app.models.models import Produtor
from brain_app.schemas.produtor_schema import ProdutorCreate, ProdutorUpdate

class ProdutorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, produtor_id: int) -> Produtor | None:
        return self.db.query(Produtor).filter(Produtor.id == produtor_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Produtor]:
        return self.db.query(Produtor).offset(skip).limit(limit).all()

    def create(self, produtor_create: ProdutorCreate) -> Produtor:
        db_produtor = Produtor(
            cpf_cnpj=produtor_create.cpf_cnpj,
            nome_produtor=produtor_create.nome_produtor,
        )
        self.db.add(db_produtor)
        self.db.commit()
        self.db.refresh(db_produtor)
        return db_produtor

    def update(self, produtor_db: Produtor, produtor_update: ProdutorUpdate) -> Produtor:
        if produtor_update.cpf_cnpj is not None:
            produtor_db.cpf_cnpj = produtor_update.cpf_cnpj
        if produtor_update.nome_produtor is not None:
            produtor_db.nome_produtor = produtor_update.nome_produtor

        self.db.commit()
        self.db.refresh(produtor_db)
        return produtor_db

    def delete(self, produtor_db: Produtor) -> None:
        self.db.delete(produtor_db)
        self.db.commit()
