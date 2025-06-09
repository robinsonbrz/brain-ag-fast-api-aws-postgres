from typing import Optional

from pydantic import BaseModel, ConfigDict, condecimal, constr, model_validator


class FazendaBaseSchema(BaseModel):
    nome_fazenda: constr(min_length=1, max_length=100)
    cidade: constr(min_length=1, max_length=100)
    estado: constr(min_length=2, max_length=2)
    area_total: condecimal(gt=0)
    area_agricultavel: condecimal(ge=0)
    area_vegetacao: condecimal(ge=0)

    @model_validator(mode="after")
    def check_area(cls, model):
        if model.area_agricultavel + model.area_vegetacao > model.area_total:
            raise ValueError("A soma da área agricultável e vegetação não pode ultrapassar a área total.")
        return model


class FazendaCreateSchema(FazendaBaseSchema):
    produtor_id: int


class FazendaUpdateSchema(BaseModel):
    nome_fazenda: Optional[constr(min_length=1, max_length=100)] = None
    cidade: Optional[constr(min_length=1, max_length=100)] = None
    estado: Optional[constr(min_length=2, max_length=2)] = None
    area_total: Optional[condecimal(gt=0)] = None
    area_agricultavel: Optional[condecimal(ge=0)] = None
    area_vegetacao: Optional[condecimal(ge=0)] = None

    @model_validator(mode="after")
    def check_area(cls, model):
        if (
            model.area_total is not None
            and model.area_agricultavel is not None
            and model.area_vegetacao is not None
        ):
            if model.area_agricultavel + model.area_vegetacao > model.area_total:
                raise ValueError("A soma da área agricultável e vegetação não pode ultrapassar a área total.")
        return model


class FazendaReadSchema(FazendaBaseSchema):
    id: int
    produtor_id: int

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)
