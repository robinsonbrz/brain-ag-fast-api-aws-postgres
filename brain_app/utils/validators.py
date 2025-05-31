from validate_docbr import CPF, CNPJ

cpf_validator = CPF()
cnpj_validator = CNPJ()

def validar_cpf(valor: str) -> bool:
    valor = limpar_mascara(valor)
    return cpf_validator.validate(valor)

def validar_cnpj(valor: str) -> bool:
    valor = limpar_mascara(valor)
    return cnpj_validator.validate(valor)

def limpar_mascara(valor: str) -> str:
    return valor.replace('.', '').replace('-', '').replace('/', '').strip()
