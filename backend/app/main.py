from fastapi import FastAPI
from app.db import db_ok
from app.routes_profiles import router as profiles_router

app = FastAPI(title="Backend API")

app.include_router(profiles_router)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/db/health")
def db_health():
    return {"ok": db_ok()}
