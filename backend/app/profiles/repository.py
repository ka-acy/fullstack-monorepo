from sqlalchemy import Engine, text


class ProfilesRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def list_profiles(self) -> list[dict]:
        with self.engine.connect() as conn:
            rows = conn.execute(
                text(
                    """
                    select id::text as id, email, display_name, created_at
                    from public.profiles
                    order by created_at desc
                    limit 50
                    """
                )
            ).mappings().all()
        return [dict(r) for r in rows]

    def create_profile(self, email: str | None, display_name: str | None) -> dict:
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """
                    insert into public.profiles (email, display_name)
                    values (:email, :display_name)
                    returning id::text as id, email, display_name, created_at
                    """
                ),
                {"email": email, "display_name": display_name},
            ).mappings().one()
        return dict(row)

    def get_by_id(self, user_id: str) -> dict | None:
        with self.engine.connect() as conn:
            row = conn.execute(
                text(
                    """
                    select id::text as id, email, display_name, created_at
                    from public.profiles
                    where id = cast(:user_id as uuid)
                    """
                ),
                {"user_id": user_id},
            ).mappings().one_or_none()
        return dict(row) if row else None

    def update_display_name(self, user_id: str, display_name: str | None) -> dict | None:
        with self.engine.begin() as conn:
            row = conn.execute(
                text(
                    """
                    update public.profiles
                    set display_name = :display_name
                    where id = cast(:user_id as uuid)
                    returning id::text as id, email, display_name, created_at
                    """
                ),
                {"user_id": user_id, "display_name": display_name},
            ).mappings().one_or_none()
        return dict(row) if row else None
