from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from brain_app.models.models import Cultura, Fazenda
from brain_app.repositories.cultura_repository import CulturaRepository
from brain_app.schemas.cultura_schema import CulturaCreateSchema, CulturaUpdateSchema


class CulturaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CulturaRepository(db)

    def get_cultura(self, cultura_id: int) -> Cultura | None:
        return self.repo.get_by_id(cultura_id)

    def get_culturas(self, skip: int = 0, limit: int = 100) -> list[Cultura]:
        return self.repo.get_all(skip=skip, limit=limit)

    def create_cultura(self, cultura_create: CulturaCreateSchema) -> Cultura:
        try:
            fazenda = self.db.query(Fazenda).filter(Fazenda.id == cultura_create.fazenda_id).first()
            if not fazenda:
                raise ValueError("Fazenda não encontrada")
            area_plantada_total = (
                self.db.query(func.coalesce(func.sum(Cultura.area_plantada), 0))
                .filter(Cultura.fazenda_id == cultura_create.fazenda_id)
                .scalar()
            )
            nova_area_total = area_plantada_total + cultura_create.area_plantada
            if nova_area_total > fazenda.area_agricultavel:
                raise ValueError(
                    f"A soma da área plantada das culturas ({nova_area_total}) ultrapassa a área "
                    f"agricultável da fazenda ({fazenda.area_agricultavel})."
                )

            return self.repo.create(cultura_create)
        except IntegrityError as e:
            raise ValueError(f"Cultura com mesmo nome, ano e fazenda já cadastrada./n{e}")

    def update_cultura(self, cultura_id: int, cultura_update: CulturaUpdateSchema) -> Cultura:
        cultura_db = self.repo.get_by_id(cultura_id)
        if not cultura_db:
            raise ValueError("Cultura não encontrada")
        return self.repo.update(cultura_db, cultura_update)

    def delete_cultura(self, cultura_id: int) -> None:
        cultura_db = self.repo.get_by_id(cultura_id)
        if not cultura_db:
            raise ValueError("Cultura não encontrada")
        self.repo.delete(cultura_db)

    def get_culturas_por_fazenda(self, fazenda_id: int, skip: int = 0, limit: int = 100) -> list[Cultura]:
        return self.repo.get_culturas_by_fazenda_id(fazenda_id, skip, limit)
