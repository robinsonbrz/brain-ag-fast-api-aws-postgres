from sqlalchemy import func
from sqlalchemy.orm import Session

from brain_app.models.models import Cultura, Fazenda
from brain_app.schemas.dashboard_schema import DashboardResponse


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_data(self) -> DashboardResponse:
        total_fazendas_cadastradas = self.db.query(func.count(Fazenda.id)).scalar() or 0
        total_area_registrada = self.db.query(func.sum(Fazenda.area_total)).scalar() or 0

        fazendas_por_estado = (
            self.db.query(Fazenda.estado, func.count(Fazenda.id)).group_by(Fazenda.estado).all()
        )
        culturas_plantadas = (
            self.db.query(Cultura.nome_cultura, func.sum(Cultura.area_plantada))
            .group_by(Cultura.nome_cultura)
            .all()
        )
        total_agricultavel = self.db.query(func.sum(Fazenda.area_agricultavel)).scalar() or 0
        total_vegetacao = self.db.query(func.sum(Fazenda.area_vegetacao)).scalar() or 0

        return DashboardResponse(
            total_fazendas_cadastradas=total_fazendas_cadastradas,
            total_area_registrada=float(total_area_registrada),
            fazendas_por_estado=[{"estado": e, "quantidade": q} for e, q in fazendas_por_estado],
            culturas_plantadas=[
                {"nome_cultura": n, "area_plantada": float(a or 0)} for n, a in culturas_plantadas
            ],
            uso_solo=[
                {"tipo": "Agricultável", "area": float(total_agricultavel)},
                {"tipo": "Vegetação", "area": float(total_vegetacao)},
            ],
        )
