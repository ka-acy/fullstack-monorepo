import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Always load backend/.env no matter where uvicorn is started from
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(f"DATABASE_URL is not set. Expected in {env_path}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def db_ok() -> bool:
    with engine.connect() as conn:
        conn.execute(text("select 1"))
    return True
