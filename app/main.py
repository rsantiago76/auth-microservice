from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from sqlalchemy import text

from .settings import settings
from .db import engine, Base
from .routers.auth import router as auth_router
from .routers.users import router as users_router, admin as admin_router

log = logging.getLogger("uvicorn.error")

# 1️⃣ Create the FastAPI app FIRST
app = FastAPI(title="Auth Microservice", version="1.0.0")

# 2️⃣ Startup hook goes IMMEDIATELY AFTER
@app.on_event("startup")
def on_startup():
    last_err = None
    for attempt in range(1, 8):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            log.info("DB connected + tables ensured.")
            return
        except Exception as e:
            last_err = e
            log.warning(f"DB init attempt {attempt}/7 failed; retrying in 5s...")
            time.sleep(5)

    log.exception("DB init failed after retries: %s", last_err)

# 3️⃣ Middleware comes AFTER startup hook
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4️⃣ Routes last
@app.get("/health")
def health():
    return {"status": "ok"}

from sqlalchemy import text

@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)



