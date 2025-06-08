from dataclasses import dataclass
from decimal import Decimal

import pytest
from pydantic import ValidationError

from brain_app.schemas.cultura_schema import CulturaCreateSchema, CulturaReadSchema, CulturaUpdateSchema


@dataclass
class Dummy:
    id: int
    nome_cultura: str
    ano_safra: int
    area_plantada: Decimal
    fazenda_id: int


class TestCulturaSchema:

    def test_cultura_create_valid(self):
        data = {
            "nome_cultura": "Soja",
            "ano_safra": 2023,
            "area_plantada": Decimal("100.50"),
            "fazenda_id": 1,
        }
        cultura = CulturaCreateSchema(**data)
        assert cultura.nome_cultura == "Soja"
        assert cultura.ano_safra == 2023
        assert cultura.area_plantada == Decimal("100.50")
        assert cultura.fazenda_id == 1

    def test_cultura_create_invalid_nome(self):
        data = {"nome_cultura": "", "ano_safra": 2023, "area_plantada": Decimal("100.50"), "fazenda_id": 1}
        with pytest.raises(ValidationError):
            CulturaCreateSchema(**data)

    def test_cultura_create_invalid_ano_safra(self):
        data = {
            "nome_cultura": "Milho",
            "ano_safra": 1800,
            "area_plantada": Decimal("100.50"),
            "fazenda_id": 1,
        }
        with pytest.raises(ValidationError):
            CulturaCreateSchema(**data)

    def test_cultura_create_invalid_area(self):
        data = {"nome_cultura": "Milho", "ano_safra": 2023, "area_plantada": Decimal("-10"), "fazenda_id": 1}
        with pytest.raises(ValidationError):
            CulturaCreateSchema(**data)

    def test_cultura_update_requires_all_fields(self):
        data = {"nome_cultura": "Milho"}
        with pytest.raises(ValidationError):
            CulturaUpdateSchema(**data)

    def test_cultura_read_model(self):
        dummy = Dummy(1, "Soja", 2023, Decimal("100.5"), 2)
        cultura_read = CulturaReadSchema.model_validate(dummy, from_attributes=True)
        assert cultura_read.id == 1
        assert cultura_read.nome_cultura == "Soja"
        assert cultura_read.ano_safra == 2023
        assert cultura_read.area_plantada == Decimal("100.5")
        assert cultura_read.fazenda_id == 2
