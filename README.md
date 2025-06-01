# Produtores Rurais API

API REST para gerenciamento de produtores rurais, fazendas e culturas plantadas.

---

## 📋 Funcionalidades

- Cadastro, edição, remoção de produtores rurais (com validação de CPF/CNPJ).  
- Gestão de fazendas com controle de áreas (total, agricultável, vegetação).  
- Registro de culturas por fazenda e safra, com controle de área plantada.  
- Dashboard com dados agregados para visualização de estatísticas.  
- Testes unitários e integrados para garantir qualidade.  
- Logs estruturados para monitoramento e diagnóstico.  
- Dockerizado para fácil deploy e ambiente isolado.
- Deploy disparado pelo Github Actions, Terraform em AWS Lambda
- Banco de Dados local containerizado
- Banco de Dados Supabase para POC
![Fluxo Git Lambda](assets/fluxo-terraform-git-actions.png)

---

## 🛠️ Tecnologias

- Python 3.11  
- FastAPI  
- Swagger
- SQLAlchemy ORM  
- Pydantic para validação de dados  
- PostgreSQL (Tembo.io para produção)  
- Docker & Docker Compose  
- Pytest para testes  
- AWS Lambda (preparado para deployment)
- Terraform
- Github Actions
- Xubuntu Linux

---
- ![Fluxo Git Lambda](assets/swagger.png)

## 🚀 Como executar localmente

### Pré-requisitos

- Docker e Docker Compose instalados  
- Python 3.11 (opcional, para rodar local sem Docker)
- Recomendo a utilização do Linux, mas é possível adapatar para executar com Windows

### Passos

1. Clone o repositório:

```bash
git clone https://github.com/robinsonbrz/brain-ag-fast-api-aws-postgres.git
cd brain-ag-fast-api-aws-postgres
```

2. Crie o arquivo `.env` com as variáveis do banco de dados conforme (.env.example):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
DATABASE_URL=postgresql://postgres:password@db:5432/postgres
```

3. Inicie os containers Docker (API + Postgres):

```bash
docker-compose -f docker-compose-dev.yml down
docker-compose -f docker-compose-dev.yml up -d --build
docker exec -ti brain-ag_api_1 uvicorn brain_app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Acesse a API em: `http://localhost:8000`

5. Documentação interativa automática padrão OpenApi disponível em:  
`http://localhost:8000/docs` e em `http://localhost:8000/docs`

---

## 🔧 Testes

Os testes são executados sobre o **Postgres containerizado local**, devido a configuração em **tests/conftest.py**

Comandos para rodar os testes:

- Rodar todos os testes e mostrar saída detalhada:

```bash
docker exec -ti brain-ag_api_1 pytest -sv
```

- Rodar testes com relatório de cobertura no terminal:

```bash
pytest --cov=brain_app --cov-report=term tests/
```

- Gerar relatório de cobertura em HTML:

```bash
docker exec -ti brain-ag_api_1 pytest --cov=brain_app --cov-report=html tests/
```

Depois, abra o arquivo `htmlcov/index.html` no navegador para visualizar o relatório.

---

## 🛠️ Comandos úteis com Makefile

Para facilitar o gerenciamento do projeto, criei um `Makefile` com os comandos principais. Abaixo, como utilizá-los:

### Build e start dos containers Docker

```bash
make start
```

* Este comando irá parar qualquer container rodando e recriar os containers da aplicação e banco (modo detached).

### Parar os containers

```bash
make stop
```

* Encerra e remove os containers Docker relacionados ao projeto.

### Executar os testes

```bash
make test
```

* Roda os testes dentro do container `api` com saída detalhada.

### Gerar relatório de cobertura e abrir no navegador - (abre html automaticamente Linux/Mac xdg)

```bash
make coverage
```

* Executa os testes com cobertura de código, gera relatório em HTML e tenta abrir automaticamente no navegador.
* Caso o navegador não abra automaticamente, acesse o arquivo manualmente em `htmlcov/index.html`.

---

### Observações

* Para que os comandos funcionem, certifique-se de estar na raiz do projeto, onde está o `Makefile` e o `docker-compose.yml`.
* O comando `make coverage` requer que você tenha um navegador padrão configurado no sistema para abrir o relatório HTML automaticamente.
* Se estiver usando Windows, o comando `xdg-open` pode não funcionar — abra o arquivo manualmente no caminho acima.

---

## ⚙️ Estrutura do Projeto

```
brain_app/
├── api/               # Rotas FastAPI
├── core/              # Configurações centrais (db, logging, middleware)
├── models/            # Modelos SQLAlchemy
├── repositories/      # Acesso a dados
├── schemas/           # Schemas Pydantic para validação e serialização
├── services/          # Lógica de negócio
tests/
├── integration/       # Testes integrados
├── unit/              # Testes unitários
infra-lambda           # Arquivos Terraform
Dockerfile             # Arquivo criação de imagem para deploy
Dockerfile.dev         # Arquivo criação de imagem para Desenvolvimento Local
README.md
```

---

## ☁️ Deploy

A API está preparada para deployment em AWS Lambda e outros ambientes em nuvem.

Para essa POC utilizei Supabase que tem uma configuração semelhante a essa, fictícia.


```env
DATABASE_URL=postgresql://postgres.password:odsood0d034o3lk@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

Para que a pipeline Github Actions funcione é necessário adicionar essa variável em Github Repo Secrets

Existe uma documentação adicional sobre como foi configurado o Terraform em 
[infra-lambda/README-TF.md](infra-lambda/README-TF.md)

---

Quando o deploy for bem sucedido nos logs do Terraform apply é possível encontrar a url da api Lambda.

![Url Lambda](assets/url-terraform.png)


No caso do último deploy a url foi:

https://e6tapmvglgzukwqjoyzafqh2cm0rtidz.lambda-url.us-east-1.on.aws

Então o swagger e docs podem ser acessados em:

https://e6tapmvglgzukwqjoyzafqh2cm0rtidz.lambda-url.us-east-1.on.aws/redoc

https://e6tapmvglgzukwqjoyzafqh2cm0rtidz.lambda-url.us-east-1.on.aws/docs
---

## 📞 Contato

  <div>
   
  <div align="center">
    <table>
        </tr>
            <td>
                <a  href="https://www.linkedin.com/in/robinsonbrz/">
                <img src="https://raw.githubusercontent.com/robinsonbrz/robinsonbrz/main/static/img/linkedin.png" width="50" height="50">
            </td>
            <td>
                <a  href="https://www.linkedin.com/in/robinsonbrz/">
                <img  src="https://avatars.githubusercontent.com/u/18150643?s=96&amp;v=4" alt="@robinsonbrz" width="50" height="50">
            </td>
            <td>
                <a href="https://www.enedino.com.br/contato">
                <img src="https://raw.githubusercontent.com/robinsonbrz/robinsonbrz/main/static/img/gmail.png" width="50" height="50" ></a>
            </td>
        </tr>
    </table> 
  </div>
  <br>
</div>
