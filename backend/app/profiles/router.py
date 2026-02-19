from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.db import engine
from app.deps import get_current_user
from app.profiles.repository import ProfilesRepository
from app.profiles.schemas import (
    ProfileListResponse,
    ProfileRead,
    ProfileUpdate,
)
from app.profiles.service import ProfilesService


router = APIRouter(prefix="/profiles", tags=["profiles"])


def get_profiles_service() -> ProfilesService:
    return ProfilesService(repository=ProfilesRepository(engine=engine))


def _require_user_id(user: dict) -> str:
    user_id = user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing sub claim")
    return user_id


@router.get("/", response_model=ProfileListResponse)
def list_profiles(
    user: Annotated[dict, Depends(get_current_user)],
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileListResponse:
    user_id = _require_user_id(user)
    profile = service.get_profile_by_id(user_id)
    return ProfileListResponse(items=[profile] if profile else [])


@router.get("/me", response_model=ProfileRead)
def get_my_profile(
    user: Annotated[dict, Depends(get_current_user)],
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileRead:
    user_id = _require_user_id(user)

    profile = service.get_profile_by_id(user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile

@router.patch("/me", response_model=ProfileRead)
def update_my_profile(
    payload: ProfileUpdate,
    user: Annotated[dict, Depends(get_current_user)],
    service: Annotated[ProfilesService, Depends(get_profiles_service)],
) -> ProfileRead:
    user_id = _require_user_id(user)

    updated = service.update_profile(user_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")

    return updated
