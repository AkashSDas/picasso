# Picasso Backend

## Getting Started

Setup poetry environment:

```bash
poetry shell
poetry install
```

Run server:

```bash
uvicorn app.main:app --reload
```

## Database

Run Postgres via Docker:

```bash
 docker run \
  --rm   \
  --name postgres \
  -p 5555:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -d postgres:14
```

Connect to Postgres via CLI:

```bash
docker exec -it postgres psql -U postgres
```
