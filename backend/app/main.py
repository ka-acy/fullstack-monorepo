from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import db_ok
from app.deps import get_current_user
from app.profiles.router import router as profiles_router


app = FastAPI(title="Backend API")
app.include_router(profiles_router)

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "ok": True,
        "user_id": user.get("sub"),
        "email": user.get("email"),
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/db/health")
def db_health():
    return {"ok": db_ok()}
