from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.db import engine
from app.profiles.repository import ProfilesRepository
from app.profiles.schemas import ProfileCreate, ProfileListResponse, ProfileRead
from app.profiles.service import ProfilesService

router = APIRouter(prefix="/profiles", tags=["profiles"])


def get_profiles_service() -> ProfilesService:
    return ProfilesService(repository=ProfilesRepository(engine=engine))


@router.get("/", response_model=ProfileListResponse)
def list_profiles(
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileListResponse:
    return service.list_profiles()


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: ProfileCreate,
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileRead:
    return service.create_profile(payload)
