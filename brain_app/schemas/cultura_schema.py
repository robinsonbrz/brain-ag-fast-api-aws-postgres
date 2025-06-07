from typing import Optional

from pydantic import BaseModel, ConfigDict, condecimal, conint, constr


class CulturaBaseSchema(BaseModel):
    nome_cultura: constr(min_length=1, max_length=100)
    ano_safra: conint(gt=1900)
    area_plantada: condecimal(gt=0)


class CulturaCreateSchema(CulturaBaseSchema):
    fazenda_id: int


class CulturaUpdateSchema(BaseModel):
    nome_cultura: Optional[constr(min_length=1, max_length=100)]
    ano_safra: Optional[conint(gt=1900)]
    area_plantada: Optional[condecimal(gt=0)]


class CulturaReadSchema(CulturaBaseSchema):
    id: int
    fazenda_id: int

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)
