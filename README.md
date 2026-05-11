# 🌿 MOA — Backend API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-14%2B-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Alembic-migrations-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/licença-proprietária-red?style=for-the-badge"/>
</p>

> **MOA** é um marketplace mobile dedicado a artesanatos e produtos culturais de povos indígenas da América Latina — conectando comunidades tradicionais a consumidores conscientes com respeito, dignidade e valorização cultural.

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Stack de Tecnologias](#-stack-de-tecnologias)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Rodando com Docker](#-rodando-com-docker)
- [Migrations com Alembic](#-migrations-com-alembic)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Endpoints da API](#-endpoints-da-api)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença-e-direitos-de-uso)

---

## 🧭 Sobre o Projeto

O **MOA** nasce do compromisso de preservar e valorizar a riqueza cultural dos povos originários da América Latina. A plataforma permite que artesãos e comunidades indígenas cadastrem, descrevam e vendam seus produtos com autonomia — preservando a autenticidade e a história por trás de cada peça.

Este repositório contém a **API backend**, construída em **FastAPI**, responsável por toda a lógica de negócio, autenticação, gerenciamento de produtos, pedidos e integração com serviços externos.

**Principais funcionalidades:**

- 🛒 Cadastro e gerenciamento de produtos artesanais
- 👤 Autenticação e autorização (JWT)
- 🏪 Perfis de vendedor (comunidades/artesãos) e comprador
- 📦 Gestão de pedidos e histórico de transações
- 🔔 Sistema de notificações
- 🌍 Suporte a múltiplas regiões e culturas da América Latina

---

## 🛠 Stack de Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Framework Web | FastAPI |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Banco de Dados | PostgreSQL 14+ |
| Validação | Pydantic v2 |
| Servidor ASGI | Uvicorn |
| Containerização | Docker + Docker Compose |
| Testes | Pytest + httpx |
| Lint   | Ruff |

---

## 🏗 Arquitetura

O projeto é estruturado em módulos:

```
moa-backend/
├── app/
│   ├── main.py                     # Entrypoint da aplicação FastAPI
│
│   ├── core/                       # Configuração central do sistema
│   │   ├── config.py               # Settings (env, Pydantic Settings)
│
│   ├── shared/                     # Código reutilizável entre módulos
│   │   ├── infrastructure/         # DB, base models, session, etc.
│   │   ├── presentation/           # Middlewares, exceptions globais
│   │   └── domain/                 # Base entities/interfaces (se usar)
│
│   ├── modules/                   # Módulos de domínio (feature-based)
│   │   ├── auth/
│   │   │   ├── domain/             # Entidades e regras de negócio
│   │   │   ├── application/        # Use cases / serviços de aplicação
│   │   │   ├── infrastructure/     # Models, repositories (SQLAlchemy)
│   │   │   └── presentation/       # Routes, schemas, middlewares
│   │   │
│   │   └── products/
│   │       ├── domain/
│   │       ├── application/
│   │       ├── infrastructure/
│           └── presentation/
│
│
├── alembic/
│   ├── versions/                   # Migrations geradas
│   └── env.py                     # Config do Alembic
│
├── tests/                         # Testes organizados por módulo
│
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) *(opcional, mas recomendado)*
- [Git](https://git-scm.com/)

---

## 🚀 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/sua-org/moa-backend.git
cd moa-backend
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com as suas credenciais (veja a seção [Variáveis de Ambiente](#-variáveis-de-ambiente)).

### 5. Execute as migrations

```bash
alembic upgrade head
```

### 6. Inicie o servidor de desenvolvimento

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`  
Documentação interativa (Swagger): `http://localhost:8000/docs`  
Documentação alternativa (ReDoc): `http://localhost:8000/redoc`

---

## 🐳 Rodando com Docker

A forma mais simples de subir toda a stack (API + banco de dados) é via Docker Compose.

### Subir todos os serviços

```bash
docker-compose up --build
```

### Subir em segundo plano (modo detached)

```bash
docker-compose up -d --build
```

### Parar os serviços

```bash
docker-compose down
```

### Parar e remover volumes (apaga o banco)

```bash
docker-compose down -v
```

### Ver logs da API

```bash
docker-compose logs -f api
```
---

## 🗃 Migrations com Alembic

O projeto usa **Alembic** para controle de versão do banco de dados.

### Criar uma nova migration

Após alterar ou criar um modelo SQLAlchemy, gere a migration automaticamente:

```bash
alembic revision --autogenerate -m "descricao_da_alteracao"
```

### Aplicar todas as migrations pendentes

```bash
alembic upgrade head
```

### Aplicar uma migration específica

```bash
alembic upgrade <revision_id>
```

### Reverter a última migration

```bash
alembic downgrade -1
```

### Reverter até uma migration específica

```bash
alembic downgrade <revision_id>
```

### Ver o histórico de migrations

```bash
alembic history --verbose
```

### Ver a migration atual aplicada no banco

```bash
alembic current
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```env
# Application
APP_NAME=FastAPI Clean Architecture
VERSION=1.0.0
ENVIRONMENT=development
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/moa_db
DB_ECHO=False
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=12

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# Rate Limiting
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=60

# Logging
LOG_LEVEL=INFO
```

> ⚠️ **Nunca commite o arquivo `.env` no repositório.** Ele já está listado no `.gitignore`.

---

## 📡 Endpoints da API

Após subir a aplicação, a documentação completa e interativa está disponível em:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🧪 Testes

### Rodar todos os testes

```bash
pytest
```

### Rodar com cobertura de código

```bash
pytest --cov=app --cov-report=term-missing
```

### Rodar um arquivo ou teste específico

```bash
pytest tests/test_products.py
pytest tests/test_auth.py::test_login_success
```

---

## 🤝 Contribuindo

Este projeto é de acesso restrito aos colaboradores autorizados da equipe MOA. Para contribuir:

1. Certifique-se de estar na lista de colaboradores autorizados
2. Crie uma branch a partir de `develop`:
   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```
3. Faça seus commits seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: adiciona endpoint de avaliação de produtos"
   ```
4. Abra um Pull Request para a branch `develop` com uma descrição clara das alterações
5. Aguarde revisão de pelo menos um membro do time antes do merge

---

## 📄 Licença e Direitos de Uso

**Copyright © 2024 Equipe MOA — Todos os direitos reservados.**

Este projeto é **propriedade exclusiva da equipe MOA** e seu uso é restrito aos colaboradores formalmente autorizados, exclusivamente para fins de desenvolvimento do aplicativo MOA.

É **expressamente proibido**:

- Vender, licenciar ou comercializar este código ou qualquer parte dele
- Redistribuir, copiar ou publicar o código-fonte, total ou parcialmente
- Utilizar este projeto, integral ou parcialmente, para fins comerciais sem autorização prévia e por escrito
- Reutilizar componentes, módulos ou trechos deste repositório em outros projetos, públicos ou privados
- Fazer engenharia reversa com fins de replicação ou concorrência

O uso não autorizado poderá resultar em responsabilização civil e criminal conforme a **Lei nº 9.610/1998 (Lei de Direitos Autorais)** e demais legislações brasileiras e internacionais aplicáveis.

Para solicitações de uso, entre em contato com a equipe através dos canais oficiais do projeto.

---

<p align="center">
  Feito com 🌿 pela equipe MOA — valorizando culturas, conectando pessoas.
</p>
