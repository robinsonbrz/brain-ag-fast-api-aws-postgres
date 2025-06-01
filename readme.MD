popular um arquivo .env conforme o exemplo .env.example
possibilidade de utilizar um MAKEFILE
docker-compose up --build

docker-compose run api pytest

clear && pytest -s  tests
# -v -q -s

#Todo validação de CPF e CNPJ
#validar cpf e cnpj invalidos 
# utilizar faker
# tentar associar uma fazenda a um produtor id não existen99e
# aprimorar testes
# aplicar linters

#TODO teste put com areas incompativeis

# Makefile para testes e build dos containers


pytest --cov=brain_app --cov-report=term tests/

pytest --cov=brain_app --cov-report=html tests/

htmlcov/index.html

        