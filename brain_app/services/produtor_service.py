from sqlalchemy.orm import Session
from brain_app.repositories.produtor_repository import ProdutorRepository
from brain_app.schemas.produtor_schema import ProdutorCreate, ProdutorUpdate
from brain_app.models.models import Produtor

class ProdutorService:
    def __init__(self, db: Session):
        self.repo = ProdutorRepository(db)

    def get_produtor_por_cpf_cnpj(self, cpf_cnpj: str) -> Produtor | None:
        return self.repo.get_by_cpf_cnpj(cpf_cnpj)

    def get_produtores(self, skip: int = 0, limit: int = 100) -> list[Produtor]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_produtor(self, produtor_create: ProdutorCreate) -> Produtor:
        existing = self.repo.db.query(Produtor).filter(Produtor.cpf_cnpj == produtor_create.cpf_cnpj).first()
        if existing:
            raise ValueError("Produtor com esse CPF/CNPJ já existe")

        return self.repo.create(produtor_create)

    def update_produtor(self, produtor_id: int, produtor_update: ProdutorUpdate) -> Produtor:
        produtor_db = self.repo.get_by_id(produtor_id)
        if not produtor_db:
            raise ValueError("Produtor não encontrado")

        if produtor_update.cpf_cnpj:
            existing = self.repo.db.query(Produtor).filter(
                Produtor.cpf_cnpj == produtor_update.cpf_cnpj,
                Produtor.id != produtor_id
            ).first()
            if existing:
                raise ValueError("Outro produtor com esse CPF/CNPJ já existe")

        return self.repo.update(produtor_db, produtor_update)
    
    def update_produtor_por_cpf_cnpj(self, cpf_cnpj: str, produtor_update: ProdutorUpdate) -> Produtor:
        produtor_db = self.repo.get_by_cpf_cnpj(cpf_cnpj)
        if not produtor_db:
            raise ValueError("Produtor não encontrado")
 
        return self.repo.update_by_cpf_cnpj(cpf_cnpj, produtor_update)

    def delete_produtor_por_cpf_cnpj(self, cpf_cnpj: str) -> None:
        self.repo.delete_by_cpf_cnpj(cpf_cnpj)
