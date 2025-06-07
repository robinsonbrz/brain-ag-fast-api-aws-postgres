from sqlalchemy.orm import Session

from brain_app.models.models import Fazenda
from brain_app.schemas.fazenda_schema import FazendaCreate, FazendaUpdate


class FazendaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, fazenda_id: int) -> Fazenda | None:
        return self.db.query(Fazenda).filter(Fazenda.id == fazenda_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Fazenda]:
        return self.db.query(Fazenda).offset(skip).limit(limit).all()

    def create(self, fazenda_create: FazendaCreate) -> Fazenda:
        db_fazenda = Fazenda(
            produtor_id=fazenda_create.produtor_id,
            nome_fazenda=fazenda_create.nome_fazenda,
            cidade=fazenda_create.cidade,
            estado=fazenda_create.estado,
            area_total=fazenda_create.area_total,
            area_agricultavel=fazenda_create.area_agricultavel,
            area_vegetacao=fazenda_create.area_vegetacao,
        )
        self.db.add(db_fazenda)
        self.db.commit()
        self.db.refresh(db_fazenda)
        return db_fazenda

    def update(self, fazenda_db: Fazenda, fazenda_update: FazendaUpdate) -> Fazenda:
        if fazenda_update.nome_fazenda is not None:
            fazenda_db.nome_fazenda = fazenda_update.nome_fazenda
        if fazenda_update.cidade is not None:
            fazenda_db.cidade = fazenda_update.cidade
        if fazenda_update.estado is not None:
            fazenda_db.estado = fazenda_update.estado
        if fazenda_update.area_total is not None:
            fazenda_db.area_total = fazenda_update.area_total
        if fazenda_update.area_agricultavel is not None:
            fazenda_db.area_agricultavel = fazenda_update.area_agricultavel
        if fazenda_update.area_vegetacao is not None:
            fazenda_db.area_vegetacao = fazenda_update.area_vegetacao

        self.db.commit()
        self.db.refresh(fazenda_db)
        return fazenda_db

    def delete(self, fazenda_db: Fazenda) -> None:
        self.db.delete(fazenda_db)
        self.db.commit()
