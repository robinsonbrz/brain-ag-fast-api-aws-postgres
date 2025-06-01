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



pytest --cov=brain_app --cov-report=term tests/

pytest --cov=brain_app --cov-report=html tests/

htmlcov/index.html

logs/app.log


Configuração centralizada do logger direcionado para stdout, ideal para AWS Lambda e CloudWatch.

Middleware para logging das requisições HTTP.

Estratégia para capturar e logar exceções não tratadas globalmente.

Boas práticas para logar erros específicos nas rotas e serviços.