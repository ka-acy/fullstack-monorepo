
from fastapi import APIRouter
from sqlalchemy import text

from app.db import engine

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/")
def list_profiles():
    with engine.connect() as conn:
        rows = conn.execute(
            text("select id, email, display_name, created_at from public.profiles order by created_at desc limit 50")
        ).mappings().all()
    return {"items": list(rows)}


@router.post("/")
def create_profile(email: str, display_name: str | None = None):
    with engine.begin() as conn:
        row = conn.execute(
            text(
                "insert into public.profiles (email, display_name) values (:email, :display_name) "
                "returning id, email, display_name, created_at"
            ),
            {"email": email, "display_name": display_name},
        ).mappings().one()
    return row