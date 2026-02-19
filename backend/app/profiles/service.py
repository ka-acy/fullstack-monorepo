from app.profiles.schemas import (
    ProfileCreate,
    ProfileListResponse,
    ProfileRead,
    ProfileUpdate,
)


class ProfilesService:
    def __init__(self, repository=None, repo=None):
        self.repository = repository or repo
        if self.repository is None:
            raise ValueError("ProfilesService requires a repository")

    def list_profiles(self) -> ProfileListResponse:
        items = [ProfileRead.model_validate(row) for row in self.repository.list_profiles()]
        return ProfileListResponse(items=items)

    def create_profile(self, payload: ProfileCreate) -> ProfileRead:
        row = self.repository.create_profile(
            email=payload.email,
            display_name=payload.display_name,
        )
        return ProfileRead.model_validate(row)

    def get_profile_by_id(self, user_id: str) -> ProfileRead | None:
        row = self.repository.get_by_id(user_id)
        return ProfileRead.model_validate(row) if row else None

    def update_profile(self, user_id: str, payload: ProfileUpdate) -> ProfileRead | None:
        row = self.repository.update_display_name(
            user_id=user_id,
            display_name=payload.display_name,
        )
        return ProfileRead.model_validate(row) if row else None
