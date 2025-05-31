from pydantic import ConfigDict
from pydantic import BaseModel, constr, field_validator
import re

CPF_CNPJ_REGEX = r'^\d{11}$|^\d{14}$'

class ProdutorBase(BaseModel):
    cpf_cnpj: constr(strip_whitespace=True, min_length=11, max_length=14)
    nome_produtor: constr(strip_whitespace=True, min_length=1, max_length=100)

    @field_validator('cpf_cnpj')
    def validate_cpf_cnpj(cls, v):
        # Validação simples: só números e tamanho válido (11 ou 14 dígitos)
        if not re.fullmatch(CPF_CNPJ_REGEX, v):
            raise ValueError('CPF ou CNPJ inválido')
        return v

class ProdutorCreate(ProdutorBase):
    pass

class ProdutorUpdate(BaseModel):
    cpf_cnpj: constr(strip_whitespace=True, min_length=11, max_length=14) | None = None
    nome_produtor: constr(strip_whitespace=True, min_length=1, max_length=100) | None = None

    @field_validator('cpf_cnpj')
    def validate_cpf_cnpj(cls, v):
        if v is not None and not re.fullmatch(CPF_CNPJ_REGEX, v):
            raise ValueError('CPF ou CNPJ inválido')
        return v

class ProdutorRead(ProdutorBase):
    id: int

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)
