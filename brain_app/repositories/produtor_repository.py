from sqlalchemy.orm import Session

from brain_app.models.models import Produtor
from brain_app.schemas.produtor_schema import ProdutorCreateSchema, ProdutorUpdateSchema
from brain_app.utils.validators import limpar_mascara


class ProdutorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Produtor]:
        return self.db.query(Produtor).offset(skip).limit(limit).all()

    def create(self, produtor_create: ProdutorCreateSchema) -> Produtor:
        db_produtor = Produtor(
            cpf_cnpj=produtor_create.cpf_cnpj,
            nome_produtor=produtor_create.nome_produtor,
        )
        self.db.add(db_produtor)
        self.db.commit()
        self.db.refresh(db_produtor)
        return db_produtor

    def update_by_cpf_cnpj(self, cpf_cnpj: str, produtor_update: ProdutorUpdateSchema) -> Produtor:
        cpf_cnpj_limpo = limpar_mascara(cpf_cnpj)
        produtor_db = self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj_limpo).first()
        if not produtor_db:
            raise ValueError("Produtor não encontrado")

        if produtor_update.nome_produtor:
            produtor_db.nome_produtor = produtor_update.nome_produtor

        self.db.commit()
        self.db.refresh(produtor_db)
        return produtor_db

    def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Produtor | None:
        cpf_cnpj_limpo = limpar_mascara(cpf_cnpj)
        return self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj_limpo).first()

    def delete_by_cpf_cnpj(self, cpf_cnpj: str) -> None:
        cpf_cnpj_limpo = limpar_mascara(cpf_cnpj)
        produtor_db = self.db.query(Produtor).filter(Produtor.cpf_cnpj == cpf_cnpj_limpo).first()
        if produtor_db:
            self.db.delete(produtor_db)
            self.db.commit()
