from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .settings import settings
from .db import engine, Base
from .routers.auth import router as auth_router
from .routers.users import router as users_router, admin as admin_router

log = logging.getLogger("uvicorn.error")

app = FastAPI(title="Auth Microservice", version="1.0.0")

@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        log.info("DB tables ensured.")
    except Exception as e:
        # Don’t crash the service; log and continue so /health and /docs load.
        log.exception("DB init failed on startup (will retry on next deploy): %s", e)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)


