# Backend (FastAPI)

## Run

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment

Create `backend/.env` from `backend/.env.example`.

Required vars:
- `DATABASE_URL`
- `SUPABASE_JWKS_URL`
- `SUPABASE_JWT_ISSUER`
- `SUPABASE_JWT_AUDIENCE`

## Endpoints

- `GET /`
- `GET /ping`
- `GET /db/health`
- `GET /protected` (auth required)
- `GET /profiles/` (auth required)
- `GET /profiles/me` (auth required)
- `PATCH /profiles/me` (auth required)

## Tests

```bash
uv run pytest -q
```

## Token Verification

`app/auth.py` validates:
- signing key from Supabase JWKS
- JWT algorithm (`RS256` or `ES256`)
- `aud` claim (`SUPABASE_JWT_AUDIENCE`)
- `iss` claim (`SUPABASE_JWT_ISSUER`)

If key lookup fails, JWKS cache is refreshed once to handle key rotation.
