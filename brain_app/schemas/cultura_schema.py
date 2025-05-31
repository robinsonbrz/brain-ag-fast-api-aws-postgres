from pydantic import BaseModel, constr, conint, condecimal, model_validator
from typing import Optional
from pydantic import ConfigDict

class CulturaBase(BaseModel):
    nome_cultura: constr(min_length=1, max_length=100)
    ano_safra: conint(gt=1900)
    area_plantada: condecimal(gt=0)

class CulturaCreate(CulturaBase):
    fazenda_id: int

class CulturaUpdate(BaseModel):
    nome_cultura: Optional[constr(min_length=1, max_length=100)]
    ano_safra: Optional[conint(gt=1900)]
    area_plantada: Optional[condecimal(gt=0)]

class CulturaRead(CulturaBase):
    id: int
    fazenda_id: int

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)
