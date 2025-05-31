from sqlalchemy.orm import Session
from brain_app.models.models import Produtor
from brain_app.schemas.produtor_schema import ProdutorCreate, ProdutorUpdate

class ProdutorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Produtor | None:
        return self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj).first()


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

    def update_by_cpf_cnpj(self, cpf_cnpj: str, produtor_update: ProdutorUpdate) -> Produtor:
        produtor_db = self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj).first()
        if not produtor_db:
            raise ValueError("Produtor não encontrado")
        
        if produtor_update.nome_produtor:
            produtor_db.nome_produtor = produtor_update.nome_produtor

        self.db.commit()
        self.db.refresh(produtor_db)
        return produtor_db

    def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Produtor | None:
        return self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj).first()
    
    def delete_by_cpf_cnpj(self, cpf_cnpj: str) -> None:
        produtor_db = self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj).first()
        if produtor_db:
            self.db.delete(produtor_db)
            self.db.commit()
