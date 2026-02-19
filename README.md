# fullstack-monorepo

Monorepo for a local full-stack app using:
- `frontend`: Next.js app with Supabase client auth
- `backend`: FastAPI API with JWT verification against Supabase JWKS
- `supabase`: local Supabase config + SQL migrations (profiles table, trigger, RLS)

## Prerequisites

- Node.js + npm
- Python 3.12+
- `uv` (Python package manager/runner)
- Supabase CLI

## Project Structure

- `frontend/`: UI + auth + API calls proxied to backend
- `backend/`: FastAPI API, profile endpoints, token verification
- `supabase/`: local Supabase project config and migrations

## Local Setup

### 1) Start Supabase

From repo root:

```bash
supabase start
```

Get local keys/status:

```bash
supabase status
```

### 2) Configure backend env

Create `backend/.env` from example and set values from your local Supabase:

```bash
cp backend/.env.example backend/.env
```

Required vars:
- `DATABASE_URL`
- `SUPABASE_JWKS_URL` (local default: `http://127.0.0.1:54321/auth/v1/.well-known/jwks.json`)
- `SUPABASE_JWT_ISSUER` (local default: `http://127.0.0.1:54321/auth/v1`)
- `SUPABASE_JWT_AUDIENCE` (default: `authenticated`)

### 3) Configure frontend env

Create `frontend/.env.local`:

```bash
cp frontend/.env.local.example frontend/.env.local
```

Set:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_API_BASE=/api`

### 4) Run app

From repo root:

```bash
npm run dev
```

This runs:
- backend on `http://127.0.0.1:8000`
- frontend on `http://127.0.0.1:3000`

## API Overview

Base URL (local): `http://127.0.0.1:8000`

Public:
- `GET /` health
- `GET /ping` basic ping
- `GET /db/health` database check

Authenticated (Bearer token from Supabase session):
- `GET /protected`
- `GET /profiles/` returns authenticated user's profile as list shape
- `GET /profiles/me`
- `PATCH /profiles/me` updates `display_name`

## Auth Flow

1. Frontend signs up/signs in via Supabase Auth.
2. Frontend receives access token from Supabase session.
3. Frontend sends token in `Authorization: Bearer <token>` to backend.
4. Backend verifies JWT signature + audience + issuer using Supabase JWKS.

## Database Model

`public.profiles` includes:
- `id uuid primary key`
- `created_at timestamptz`
- `email text unique`
- `display_name text`

Supabase migrations include:
- profile table creation
- auth trigger to create profile row for new users
- RLS policies for own-profile read/update

## Quality Checks

Backend tests:

```bash
cd backend && uv run pytest -q
```

Frontend lint:

```bash
cd frontend && npm run lint
```

## Common Issues

### 401 token verification failures

Check:
- `SUPABASE_JWKS_URL` path is `/.well-known/jwks.json`
- `SUPABASE_JWT_ISSUER` matches token `iss` exactly (`localhost` vs `127.0.0.1` must match)
- Supabase is running and reachable

### 404 on JWKS URL

If you see `/auth/v1/certs`, your env is wrong or stale. Use:
- `http://127.0.0.1:54321/auth/v1/.well-known/jwks.json`

Then restart backend.

# Reflection
Throughout this project, I worked iteratively with Codex to build a full-stack application while learning modern development practices step by step. Rather than passively following a static tutorial, I treated the assignment itself as a guided learning path and used Codex as a collaborative partner, going back and forth to debug issues, refine structure, and understand why certain patterns were used. As I implemented Python project structure and PEP 8 conventions, adopted UV for dependency management, configured Supabase locally, built a Next.js frontend with Tailwind, and integrated JWT-based authentication between frontend and backend, each obstacle became part of the learning process. I encountered real-world issues like environment variable overrides, incorrect JWKS endpoints, constructor mismatches, and 401 authentication errors, and worked through them interactively. This back-and-forth debugging process helped me see how the pieces connect in practice. By using the generated assignment plan as a step-by-step framework and refining it through active experimentation and troubleshooting, I turned the build process into a hands-on tutorial that deepened my understanding of full-stack architecture, authentication flows, dependency management, and development workflows.
