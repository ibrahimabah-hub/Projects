# User Behavior Analytics

A small FastAPI service for recording and querying visitor activity. The Docker
Compose deployment runs the PostgreSQL-backed application in `app/main.py`.

## Architecture and technology

```text
API client
   |
   | HTTP / JSON
   v
FastAPI + Uvicorn (app.main:app)
   |
   | SQLAlchemy / psycopg2
   v
PostgreSQL 17 (Compose service: db)
```

- **API:** FastAPI with Pydantic request models
- **Server:** Uvicorn
- **Database access:** SQLAlchemy and psycopg2
- **Database:** PostgreSQL 17 in Docker Compose, persisted in the `db_data`
  named volume
- **Alternative prototype:** `app/main_sqlite.py` and
  `database/db_schema_sqlite.py` use SQLModel and a local SQLite database.
  This is a separate, incomplete implementation and is not started by the
  provided Compose file.

At application startup, the Postgres app creates its tables from the SQLAlchemy
models. There are no configured Alembic migrations for this app.

## Data model

The following describes the Postgres models used by Docker Compose
(`database/models.py`):

| Entity/table | Fields | Meaning |
| --- | --- | --- |
| `Visitor` / `visitor` | `id` (primary key), `ip_address` | A visitor record. |
| `Visit` / `visit` | `id` (primary key), `visitor_id` (foreign key to `visitor.id`), `duration` (seconds; defaults to `0`) | One session belonging to a visitor. |
| `Hit` / `hit` | `id` (primary key), `timestamp`, `page_url`, `visit_id` (foreign key to `visit.id`) | A page activity record belonging to a visit. |
| `Product` / `product` | `id` (primary key), `category`, `brand`, `price` | Product catalog record. The current Postgres API does not expose product operations or connect hits to products. |

The intended activity hierarchy is **one visitor → many visits → many hits**.
`visit.visitor_id` links each visit to its visitor; `hit.visit_id` links each
hit to its visit. The current Postgres `Hit` model does not have a
`product_id` field, so products are independent catalog rows in that
implementation.

The SQLite prototype has a different schema: its `Product` includes
`product_id`, `type`, `brand`, `form_factor`, `category`, and `price`, and its
`Hit` model has an optional `product_id` foreign key to `product.id`. Do not
assume those fields or relationships are present in the Postgres deployment.

## Configuration

Copy the example environment file before starting the stack:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

If `.env` already exists, keep it and update its settings rather than
overwriting it. Set a private `POSTGRES_PASSWORD` in `.env` before use. Compose passes the
Postgres credentials to the database container and maps them to the lowercase
`db_user`, `db_pass`, `db_host`, and `db_name` variables read by the
application. `db_host` is set to the Compose service name `db`.

`.env` is ignored by Git and excluded from the Docker build context. Keep real
credentials only in your local `.env` or a deployment secrets manager; do not
put them in source files or commit them.

## Run locally with Docker Compose

Prerequisites: Docker Desktop (or Docker Engine) with the Compose plugin.

From this directory:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
# Edit .env and replace POSTGRES_PASSWORD with a local development secret.
docker compose up --build
```

Compose waits for PostgreSQL's health check before starting the API. The
service is available at <http://localhost:8000>. Interactive API
documentation is at <http://localhost:8000/docs>; OpenAPI JSON is at
<http://localhost:8000/openapi.json>.

Stop the services while retaining database data:

```powershell
docker compose down
```

To also remove the PostgreSQL data volume (this permanently deletes local
database data):

```powershell
docker compose down --volumes
```

The Compose configuration publishes PostgreSQL on host port `5433` for local
database clients; the API connects to it internally as `db:5432`.

## HTTP API

All paths below are served by `app/main.py`. The API currently has no product
routes.

| Method | Path | Behavior |
| --- | --- | --- |
| `GET` | `/` | Health-like greeting: `{"Hello":"World"}`. |
| `GET` | `/visitors/` | List visitors; returns `404` when none exist. |
| `GET` | `/visitors/{visitor_id}` | Get one visitor; returns `404` when not found. |
| `POST` | `/visitors/` | Create a visitor with nested visits and hits (the `visits` field may be an empty list). |
| `GET` | `/visits/` | List visits; returns `404` when none exist. |
| `GET` | `/visits/{visitor_id}` | List visits for the given **visitor** ID; returns `404` when there are none. |

### Example: greeting

```http
GET http://localhost:8000/
```

Response:

```http
HTTP/1.1 200 OK
content-type: application/json
```

```json
{"Hello":"World"}
```

### Example: create a visitor with one visit and two hits

```http
POST http://localhost:8000/visitors/
Content-Type: application/json

{
  "ip_address": "203.0.113.24",
  "visits": [
    {
      "hits": [
        {
          "timestamp": "2026-10-20T09:00:00",
          "page_url": "/home"
        },
        {
          "timestamp": "2026-10-20T09:04:30",
          "page_url": "/products"
        }
      ]
    }
  ]
}
```

The current handler creates the visitor, visit, and hits, but does not return
the created record. Its response is therefore:

```http
HTTP/1.1 200 OK
content-type: application/json
```

```json
null
```

### Example: list visitors

```http
GET http://localhost:8000/visitors/
```

Example response after creating a visitor:

```http
HTTP/1.1 200 OK
content-type: application/json
```

```json
[
  {
    "id": 1,
    "ip_address": "203.0.113.24"
  }
]
```

### Example: get visits for a visitor

```http
GET http://localhost:8000/visits/1
```

Example response:

```http
HTTP/1.1 200 OK
content-type: application/json
```

```json
[
  {
    "id": 1,
    "duration": 270.0,
    "visitor_id": 1
  }
]
```

The visitor and visit lookup/list endpoints return `404` with a JSON `detail`
message when the requested visitor or visits are not present. There is
currently no endpoint for listing hits.

## Deployment overview

The supplied Compose file builds the API image from `Dockerfile`, starts
PostgreSQL 17, waits for the database health check, and stores database files
in the `db_data` volume. This is suitable for local development and as a
starting point for deployment, not a complete production configuration. The
container command enables Uvicorn reload.

For production, build and publish a versioned image, disable reload, keep
PostgreSQL private to the application network, provide credentials through
the hosting platform's secret manager, terminate HTTPS at a reverse proxy or
load balancer, and configure persistent database storage and backups. Plan
schema migrations before evolving the database; the current app creates
tables at startup but does not apply Alembic migrations.
