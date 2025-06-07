from typing import List

from pydantic import BaseModel


class EstadoQuantidade(BaseModel):
    estado: str
    quantidade: int


class CulturaArea(BaseModel):
    nome_cultura: str
    area_plantada: float


class UsoSoloArea(BaseModel):
    tipo: str
    area: float


class DashboardResponse(BaseModel):
    total_fazendas_cadastradas: int
    total_area_registrada: float
    fazendas_por_estado: List[EstadoQuantidade]
    culturas_plantadas: List[CulturaArea]
    uso_solo: List[UsoSoloArea]
