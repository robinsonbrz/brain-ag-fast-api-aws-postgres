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

---

## 🛠️ Tecnologias

- Python 3.11  
- FastAPI  
- SQLAlchemy ORM  
- Pydantic para validação de dados  
- PostgreSQL (Tembo.io para produção)  
- Docker & Docker Compose  
- Pytest para testes  
- AWS Lambda (preparado para deployment)

---

## 🚀 Como executar localmente

### Pré-requisitos

- Docker e Docker Compose instalados  
- Python 3.11 (opcional, para rodar local sem Docker)

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
docker-compose up --build
```

4. Acesse a API em: `http://localhost:8000`

5. Documentação interativa automática disponível em:  
`http://localhost:8000/docs` e em `http://localhost:8000/docs`

---

## 🔧 Testes

Os testes são executados sobre o **Postgres containerizado local**, devido a configuração em **tests/conftest.py**

Comandos para rodar os testes:

- Rodar todos os testes e mostrar saída detalhada:

```bash
clear && pytest -vs tests
```

- Rodar testes com relatório de cobertura no terminal:

```bash
pytest --cov=brain_app --cov-report=term tests/
```

- Gerar relatório de cobertura em HTML:

```bash
pytest --cov=brain_app --cov-report=html tests/
```

Depois, abra o arquivo `htmlcov/index.html` no navegador para visualizar o relatório.

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
Dockerfile
docker-compose.yml
README.md
```

---

## ☁️ Deploy

A API está preparada para deployment em AWS Lambda e outros ambientes em nuvem.

Para essa POC utilizei Supabase que tem uma configuração semelhante a essa, fictícia.

```env
DATABASE_URL=postgresql://postgres.password:odsood0d034o3lk@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

---

## 📞 Contato

  <div>
  <h1 align="center"> Contact </h1> 
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
