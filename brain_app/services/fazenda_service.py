from sqlalchemy.orm import Session
from brain_app.repositories.fazenda_repository import FazendaRepository
from brain_app.schemas.fazenda_schema import FazendaCreate, FazendaUpdate
from brain_app.models.models import Fazenda, Produtor

class FazendaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = FazendaRepository(db)

    def get_fazenda(self, fazenda_id: int) -> Fazenda | None:
        return self.repo.get_by_id(fazenda_id)

    def get_fazendas(self, skip: int = 0, limit: int = 100) -> list[Fazenda]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_fazenda(self, fazenda_create: FazendaCreate) -> Fazenda:
        produtor = self.db.query(Produtor).filter(Produtor.id == fazenda_create.produtor_id).first()
        if not produtor:
            raise ValueError(f"Produtor com id {fazenda_create.produtor_id} não encontrado")

        fazenda = self.repo.create(fazenda_create)
        return fazenda

    def update_fazenda(self, fazenda_id: int, fazenda_update: FazendaUpdate) -> Fazenda:
        fazenda_db = self.repo.get_by_id(fazenda_id)
        if not fazenda_db:
            raise ValueError("Fazenda não encontrada")
        return self.repo.update(fazenda_db, fazenda_update)

    def delete_fazenda(self, fazenda_id: int) -> None:
        fazenda_db = self.repo.get_by_id(fazenda_id)
        if not fazenda_db:
            raise ValueError("Fazenda não encontrada")
        self.repo.delete(fazenda_db)
