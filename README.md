# 🔐 Authentication & User Management Microservice (FastAPI)

A production-style authentication + user management microservice you can deploy as a single Render **Web Service (Docker)**.
Includes secure password hashing (bcrypt), JWT auth, and role-based access control (user/admin).

## ✅ Features
- `POST /auth/register` (email + password)
- `POST /auth/login` (JWT access token)
- `GET /users/me` (JWT required)
- `PATCH /users/me` (JWT required)
- `POST /users/change-password` (JWT required)
- `GET /admin/users` (admin only)
- `PATCH /admin/users/{id}/role` (admin only)
- `PATCH /admin/users/{id}/disable` (admin only)
- `GET /health`

## 🔧 Required Environment Variables
- `DATABASE_URL` (Postgres recommended; Render provides this for Postgres)
  - Example: `postgresql+psycopg2://user:pass@host:5432/dbname`
- `JWT_SECRET` (long random string)

## Optional Environment Variables
- `JWT_EXPIRES_MIN` (default: 15)
- `CORS_ORIGINS` (default: `*`)

## ▶️ Run Locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set DATABASE_URL + JWT_SECRET, then:
uvicorn app.main:app --reload
```

API docs:
- http://localhost:8000/docs

## ☁️ Deploy on Render
Create a **Web Service** with:
- Environment: Docker
- Docker build context: `.`
- Dockerfile: `Dockerfile`
- Health check path: `/health`

Then set env vars:
- `DATABASE_URL`
- `JWT_SECRET`
