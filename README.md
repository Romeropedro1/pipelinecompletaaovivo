# Pipeline de Automação & Dados (n8n + Python + Docker + PostgreSQL)

> Projeto modelo para orquestrar **workflows de automação** (n8n), **API em Python**, **banco PostgreSQL** e **Frontend** (opcional), tudo conteinerizado em **Docker** e com **CI/CD (GitHub Actions)**.

---

![status-badge](https://img.shields.io/badge/status-active-success)
![docker](https://img.shields.io/badge/Docker-ready-blue)
![python](https://img.shields.io/badge/Python-3.11+-yellow)
![license](https://img.shields.io/badge/license-MIT-informational)

> **Portas padrão**: API `:3333`, Frontend `:3000`, n8n `:5678`, PostgreSQL `:5432`.

---

## ✨ Visão Geral

Este repositório implementa um **pipeline completo** para:

* Expor uma **API** (Python/FastAPI) para cadastro/consulta de dados e webhooks.
* Executar **workflows de automação** no **n8n** (coleta, integração e disparo de ações).
* Persistir tudo no **PostgreSQL**.
* (Opcional) Exibir dados num **Frontend** (Next.js) em `:3000`.
* Entregar Infra como Código via **Docker Compose** e pipeline de **CI/CD**.

### Arquitetura

```
┌──────────┐    HTTP/Webhook     ┌───────────┐        ┌──────────────┐
│ Frontend │  <----------------> │   API     │  SQL   │  PostgreSQL  │
│ (3000)   │                     │ (3333)    │ <----> │   (5432)     │
└──────────┘                     └────┬──────┘        └──────────────┘
                                      │
                                Webhook/API
                                      │
                                ┌─────▼─────┐
                                │   n8n     │
                                │  (5678)   │
                                └───────────┘
```

---

## 🧱 Tecnologias

* **Python 3.11+** (FastAPI, SQLAlchemy, Alembic, Uvicorn)
* **n8n** para orquestração de workflows
* **PostgreSQL 14+**
* **Docker / Docker Compose**
* **GitHub Actions** para CI/CD
* **(Opcional)** Next.js + Tailwind CSS

---

## 📁 Estrutura de Pastas

```
.
├── api/                    # API Python (FastAPI)
│   ├── app/
│   │   ├── main.py         # Ponto de entrada FastAPI
│   │   ├── db.py           # Conexão com Postgres
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── routers/        # Rotas (ex: /health, /items, /webhook)
│   │   └── alembic/        # Migrações
│   ├── requirements.txt
│   └── Dockerfile
├── n8n_data/               # Dados do n8n (volume) – inclui workflows/
│   └── workflows/          # JSON dos fluxos exportados
├── frontend/               # (Opcional) Next.js app
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline CI
└── README.md
```

---

## ✅ Pré-requisitos

* **Docker** e **Docker Compose** instalados
* **Git** configurado
* (Opcional) **Python 3.11+** e **Node 18+** para rodar localmente sem Docker

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz a partir do modelo abaixo (`.env.example`):

```env
# Banco de Dados
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/app_db

# API
API_PORT=3333
ENV=development

# n8n
N8N_PORT=5678
N8N_HOST=0.0.0.0
N8N_BASIC_AUTH_ACTIVE=false
# N8N_BASIC_AUTH_USER=
# N8N_BASIC_AUTH_PASSWORD=

# Frontend (opcional)
FRONTEND_PORT=3000
```

> Dica: nunca commitar `.env` com credenciais reais. Use GitHub Secrets no CI.

---

## ▶️ Subir com Docker (produção/dev)

1. **Clone o repositório**

```bash
git clone https://github.com/<seu-usuario>/<seu-repo>.git
cd <seu-repo>
cp .env.example .env
```

2. **Suba os serviços**

```bash
docker compose up -d --build
```

3. **Acesse**

* API: [http://localhost:3333/docs](http://localhost:3333/docs) (Swagger)
* n8n: [http://localhost:5678](http://localhost:5678)
* Frontend (opcional): [http://localhost:3000](http://localhost:3000)

4. **Logs**

```bash
docker compose logs -f api
```

---

## 🐍 API (FastAPI) – Estrutura mínima

**api/app/main.py**

```python
from fastapi import FastAPI
from .db import init_db

app = FastAPI(title="Pipeline API")

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}
```

**api/app/db.py**

```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    # Aqui você pode rodar migrações Alembic automaticamente, se quiser
    with engine.connect() as conn:
        conn.execute("SELECT 1")
```

**api/requirements.txt**

```
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
python-dotenv
alembic
```

**api/Dockerfile**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY api /app
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3333"]
```

---

## 🧰 docker-compose.yml (exemplo completo)

```yaml
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  api:
    build:
      context: .
      dockerfile: api/Dockerfile
    environment:
      DATABASE_URL: ${DATABASE_URL}
      ENV: ${ENV}
    depends_on:
      - db
    ports:
      - "${API_PORT:-3333}:3333"
    restart: unless-stopped

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "${N8N_PORT:-5678}:5678"
    environment:
      - N8N_HOST=${N8N_HOST}
      - N8N_BASIC_AUTH_ACTIVE=${N8N_BASIC_AUTH_ACTIVE}
      # - N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
      # - N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
    volumes:
      - ./n8n_data:/home/node/.n8n
    depends_on:
      - api

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "${FRONTEND_PORT:-3000}:3000"
    depends_on:
      - api
    profiles: ["dev"]

volumes:
  pgdata:
```

> Observação: o **n8n** usa a pasta `./n8n_data` como volume permanente. Coloque seus JSONs de workflows em `n8n_data/workflows/`.

---

## 🔄 Migrações de Banco (Alembic)

1. Criar estrutura do Alembic (já incluída no template acima):

```bash
alembic init api/app/alembic
```

2. Gerar migração:

```bash
alembic revision --autogenerate -m "create initial tables"
```

3. Aplicar migrações:

```bash
alembic upgrade head
```

> Você pode automatizar no startup da API se preferir.

---

## ⚙️ Desenvolvimento local (sem Docker)

```bash
# 1) Banco
docker run --name local-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14

# 2) API
cd api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 3333

# 3) n8n
npx n8n@latest start
```

---

## 🧪 Testes & Qualidade (sugestão)

* **pytest** para testes de unidade/integrados
* **ruff/black** para lint/format

Exemplo `pyproject.toml` (API):

```toml
[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E","F","I","UP","B"]
```

---

## 🚀 CI/CD (GitHub Actions)

`.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          pip install -r api/requirements.txt
      - name: Lint & Test
        run: |
          echo "(Adicione seus linters e testes aqui)"

  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build images
        run: |
          docker build -t api:ci -f api/Dockerfile .
```

---

## 🔌 Endpoints úteis

* `GET /health` → verifica disponibilidade
* `POST /webhook/event` → recepção de eventos do n8n (exemplo; crie a rota conforme seu fluxo)

---

## 📥 Importar Workflows no n8n

* Coloque os arquivos `.json` em `n8n_data/workflows/`.
* Abra `http://localhost:5678`, **Import** → selecione o arquivo.
* Ajuste as **credenciais** pelo menu **Credentials**.

> Dica: use **HTTP Request** no n8n para chamar a API `http://api:3333/...` dentro da rede Docker.

---

## 🧩 Dicas de Produção

* Ative **N8N\_BASIC\_AUTH\_ACTIVE=true** e defina usuário/senha.
* Use **volumes** para persistência (Postgres e n8n).
* Configure **backups** do volume Postgres.
* Centralize logs com **docker logs** ou stack ELK.

---

## 🐛 Troubleshooting

* **API não sobe**: confirme `DATABASE_URL` e se o `db` está pronto (`docker compose logs db`).
* **n8n não acessa API**: use hostname `api` (rede do Compose), não `localhost`.
* **Porta em uso**: altere `API_PORT`, `N8N_PORT`, `FRONTEND_PORT` no `.env`.
* **Migração falha**: rode `alembic upgrade head` com o Postgres vivo.

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**. Sinta-se livre para usar e adaptar.

---

## 🙌 Como contribuir

1. Faça um fork
2. Crie uma branch: `feat/minha-melhoria`
3. Abra um PR descrevendo as mudanças

---

## 📝 Checklist antes de publicar no GitHub

* [ ] Atualizar **nome do repositório** e links
* [ ] Preencher `.env.example` com chaves corretas (sem segredos)
* [ ] Confirmar `docker-compose.yml` conforme seu ambiente
* [ ] Adicionar **workflows** do n8n em `n8n_data/workflows/`
* [ ] Incluir **prints ou GIF** no README (ex.: /docs/demo.gif)

