from pydantic import ConfigDict
from pydantic import BaseModel, constr, field_validator
from typing import Optional
from brain_app.utils.validators import validar_cpf, validar_cnpj, limpar_mascara


class ProdutorBase(BaseModel):
    cpf_cnpj: constr(strip_whitespace=True, min_length=11, max_length=18)  # aceita com máscara
    nome_produtor: constr(strip_whitespace=True, min_length=1, max_length=100)

    @field_validator('cpf_cnpj')
    def validate_cpf_cnpj(cls, cpf_cnpj_raw: str) -> str:
        cpf_cnpj_limpo = limpar_mascara(cpf_cnpj_raw)
        if len(cpf_cnpj_limpo) == 11:
            if not validar_cpf(cpf_cnpj_limpo):
                raise ValueError('CPF inválido')
        elif len(cpf_cnpj_limpo) == 14:
            if not validar_cnpj(cpf_cnpj_limpo):
                raise ValueError('CNPJ inválido')
        else:
            raise ValueError('CPF ou CNPJ deve ter 11 ou 14 dígitos')
        return cpf_cnpj_limpo


class ProdutorCreate(ProdutorBase):
    pass


class ProdutorUpdate(BaseModel):
    cpf_cnpj: Optional[constr(strip_whitespace=True, min_length=11, max_length=18)] = None
    nome_produtor: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = None

    @field_validator('cpf_cnpj')
    def validate_cpf_cnpj(cls, cpf_cnpj_raw: Optional[str]) -> Optional[str]:
        if cpf_cnpj_raw is None:
            return None
        cpf_cnpj_limpo = limpar_mascara(cpf_cnpj_raw)
        if len(cpf_cnpj_limpo) == 11:
            if not validar_cpf(cpf_cnpj_limpo):
                raise ValueError('CPF inválido')
        elif len(cpf_cnpj_limpo) == 14:
            if not validar_cnpj(cpf_cnpj_limpo):
                raise ValueError('CNPJ inválido')
        else:
            raise ValueError('CPF ou CNPJ deve ter 11 ou 14 dígitos')
        return cpf_cnpj_limpo


class ProdutorRead(ProdutorBase):
    id: int

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)
