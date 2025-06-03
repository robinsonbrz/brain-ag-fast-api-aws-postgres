import pytest
from brain_app.schemas.dashboard_schema import EstadoQuantidade, CulturaArea, UsoSoloArea, DashboardResponse

from pydantic import ValidationError

def test_estado_quantidade_model():
    estado_quant = EstadoQuantidade(estado="SP", quantidade=10)
    assert estado_quant.estado == "SP"
    assert estado_quant.quantidade == 10

def test_cultura_area_model():
    cultura_area = CulturaArea(nome_cultura="Soja", area_plantada=1500.5)
    assert cultura_area.nome_cultura == "Soja"
    assert cultura_area.area_plantada == 1500.5

def test_uso_solo_area_model():
    uso_solo = UsoSoloArea(tipo="Agricultura", area=2000.0)
    assert uso_solo.tipo == "Agricultura"
    assert uso_solo.area == 2000.0

def test_dashboard_response_model():
    estados = [
        EstadoQuantidade(estado="SP", quantidade=10),
        EstadoQuantidade(estado="MG", quantidade=5),
    ]
    culturas = [
        CulturaArea(nome_cultura="Soja", area_plantada=1500.5),
        CulturaArea(nome_cultura="Milho", area_plantada=800.0),
    ]
    uso_solo = [
        UsoSoloArea(tipo="Agricultura", area=2000.0),
        UsoSoloArea(tipo="Pecuária", area=300.0),
    ]

    dashboard = DashboardResponse(
        total_fazendas_cadastradas=15,
        total_area_registrada=2300.5,
        fazendas_por_estado=estados,
        culturas_plantadas=culturas,
        uso_solo=uso_solo,
    )

    assert dashboard.total_fazendas_cadastradas == 15
    assert dashboard.total_area_registrada == 2300.5

    assert len(dashboard.fazendas_por_estado) == 2
    assert dashboard.fazendas_por_estado[0].estado == "SP"
    assert dashboard.fazendas_por_estado[1].quantidade == 5

    assert len(dashboard.culturas_plantadas) == 2
    assert dashboard.culturas_plantadas[0].nome_cultura == "Soja"
    assert dashboard.culturas_plantadas[1].area_plantada == 800.0

    assert len(dashboard.uso_solo) == 2
    assert dashboard.uso_solo[0].tipo == "Agricultura"
    assert dashboard.uso_solo[1].area == 300.0
