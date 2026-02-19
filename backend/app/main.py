from fastapi import FastAPI
from app.db import db_ok
from app.profiles.router import router as profiles_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Backend API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
