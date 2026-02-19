from app.profiles.repository import ProfilesRepository
from app.profiles.schemas import ProfileCreate, ProfileListResponse, ProfileRead


class ProfilesService:
    def __init__(self, repository: ProfilesRepository) -> None:
        self._repository = repository

    def list_profiles(self) -> ProfileListResponse:
        rows = self._repository.list_profiles(limit=50)
        return ProfileListResponse(items=[ProfileRead.model_validate(row) for row in rows])

    def create_profile(self, payload: ProfileCreate) -> ProfileRead:
        row = self._repository.create_profile(payload)
        return ProfileRead.model_validate(row)
