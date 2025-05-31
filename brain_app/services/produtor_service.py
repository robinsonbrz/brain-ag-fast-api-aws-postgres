from sqlalchemy.orm import Session
from brain_app.repositories.produtor_repository import ProdutorRepository
from brain_app.schemas.produtor_schema import ProdutorCreate, ProdutorUpdate
from brain_app.models.models import Produtor
import re

CPF_CNPJ_REGEX = r'^\d{11}$|^\d{14}$'  # Simplificado

class ProdutorService:
    def __init__(self, db: Session):
        self.repo = ProdutorRepository(db)

    def get_produtor(self, produtor_id: int) -> Produtor | None:
        return self.repo.get_by_id(produtor_id)

    def get_produtores(self, skip: int = 0, limit: int = 100) -> list[Produtor]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_produtor(self, produtor_create: ProdutorCreate) -> Produtor:
        # Validação CPF/CNPJ já feita no schema, mas podemos reforçar aqui
        if not re.fullmatch(CPF_CNPJ_REGEX, produtor_create.cpf_cnpj):
            raise ValueError("CPF ou CNPJ inválido")
        # Verificar duplicidade pelo CPF/CNPJ
        existing = self.repo.db.query(Produtor).filter(Produtor.cpf_cnpj == produtor_create.cpf_cnpj).first()
        if existing:
            raise ValueError("Produtor com esse CPF/CNPJ já existe")

        return self.repo.create(produtor_create)

    def update_produtor(self, produtor_id: int, produtor_update: ProdutorUpdate) -> Produtor:
        produtor_db = self.repo.get_by_id(produtor_id)
        if not produtor_db:
            raise ValueError("Produtor não encontrado")

        if produtor_update.cpf_cnpj and not re.fullmatch(CPF_CNPJ_REGEX, produtor_update.cpf_cnpj):
            raise ValueError("CPF ou CNPJ inválido")

        # Se alterar CPF/CNPJ, verificar duplicidade
        if produtor_update.cpf_cnpj:
            existing = self.repo.db.query(Produtor).filter(
                Produtor.cpf_cnpj == produtor_update.cpf_cnpj,
                Produtor.id != produtor_id
            ).first()
            if existing:
                raise ValueError("Outro produtor com esse CPF/CNPJ já existe")

        return self.repo.update(produtor_db, produtor_update)

    def delete_produtor(self, produtor_id: int) -> None:
        produtor_db = self.repo.get_by_id(produtor_id)
        if not produtor_db:
            raise ValueError("Produtor não encontrado")
        self.repo.delete(produtor_db)
