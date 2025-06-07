from sqlalchemy.orm import Session
from brain_app.models.models import Cultura, Fazenda
from brain_app.schemas.cultura_schema import CulturaCreateSchema, CulturaUpdateSchema

class CulturaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, cultura_id: int) -> Cultura | None:
        return self.db.query(Cultura).filter(Cultura.id == cultura_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Cultura]:
        return self.db.query(Cultura).offset(skip).limit(limit).all()

    def create(self, cultura_create: CulturaCreateSchema) -> Cultura:
        fazenda = self.db.query(Fazenda).filter_by(id=cultura_create.fazenda_id).first()
        if not fazenda:
            raise ValueError("Fazenda não encontrada")
        db_cultura = Cultura(
            fazenda_id=cultura_create.fazenda_id,
            nome_cultura=cultura_create.nome_cultura,
            ano_safra=cultura_create.ano_safra,
            area_plantada=cultura_create.area_plantada,
        )
        self.db.add(db_cultura)
        self.db.commit()
        self.db.refresh(db_cultura)
        return db_cultura

    def update(self, cultura_db: Cultura, cultura_update: CulturaUpdateSchema) -> Cultura:
        if cultura_update.nome_cultura is not None:
            cultura_db.nome_cultura = cultura_update.nome_cultura
        if cultura_update.ano_safra is not None:
            cultura_db.ano_safra = cultura_update.ano_safra
        if cultura_update.area_plantada is not None:
            cultura_db.area_plantada = cultura_update.area_plantada

        self.db.commit()
        self.db.refresh(cultura_db)
        return cultura_db

    def delete(self, cultura_db: Cultura) -> None:
        self.db.delete(cultura_db)
        self.db.commit()

    def get_culturas_by_fazenda_id(self, fazenda_id: int, skip: int = 0, limit: int = 100) -> list[Cultura]:
        return (
            self.db.query(Cultura)
            .filter(Cultura.fazenda_id == fazenda_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
