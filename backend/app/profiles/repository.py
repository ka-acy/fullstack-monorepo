from collections.abc import Mapping
from typing import Any

from sqlalchemy import Engine, text

from app.profiles.schemas import ProfileCreate


class ProfilesRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def list_profiles(self, limit: int = 50) -> list[Mapping[str, Any]]:
        with self._engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        "select id, email, display_name, created_at "
                        "from public.profiles "
                        "order by created_at desc "
                        "limit :limit"
                    ),
                    {"limit": limit},
                )
                .mappings()
                .all()
            )
        return rows

    def create_profile(self, payload: ProfileCreate) -> Mapping[str, Any]:
        with self._engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "insert into public.profiles (email, display_name) "
                        "values (:email, :display_name) "
                        "returning id, email, display_name, created_at"
                    ),
                    {
                        "email": payload.email,
                        "display_name": payload.display_name,
                    },
                )
                .mappings()
                .one()
            )
        return row
