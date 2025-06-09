from faker import Faker

fake = Faker("pt_BR")


def produtor_payload():
    return {"cpf_cnpj": fake.cpf(), "nome_produtor": fake.name()}


def fazenda_payload(produtor_id, area_total=250, area_agriculturavel=150, area_vegetacao=90):
    return {
        "produtor_id": produtor_id,
        "nome_fazenda": fake.company(),
        "cidade": fake.city(),
        "estado": fake.estado_sigla(),
        "area_total": area_total,
        "area_agricultavel": area_agriculturavel,
        "area_vegetacao": area_vegetacao,
    }


def cultura_payload(fazenda_id, nome_cultura="Manga", ano_safra=2025, area_plantada=40.0):
    return {
        "fazenda_id": fazenda_id,
        "nome_cultura": nome_cultura,
        "ano_safra": ano_safra,
        "area_plantada": area_plantada,
    }


def estado_sigla():
    estados = [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ]
    return fake.random_element(estados)
