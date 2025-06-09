from typing import List

from pydantic import BaseModel


class EstadoQuantidadeSchema(BaseModel):
    estado: str
    quantidade: int


class CulturaAreaSchema(BaseModel):
    nome_cultura: str
    area_plantada: float


class UsoSoloAreaSchema(BaseModel):
    tipo: str
    area: float


class DashboardResponseSchema(BaseModel):
    total_fazendas_cadastradas: int
    total_area_registrada: float
    fazendas_por_estado: List[EstadoQuantidadeSchema]
    culturas_plantadas: List[CulturaAreaSchema]
    uso_solo: List[UsoSoloAreaSchema]
