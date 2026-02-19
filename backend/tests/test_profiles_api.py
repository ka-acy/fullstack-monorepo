from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.main import app
from app.profiles.schemas import ProfileCreate, ProfileRead
from app.profiles.service import ProfilesService


class StubProfilesRepository:
    def list_profiles(self):
        return [
            {
                "id": str(uuid4()),
                "email": "existing@example.com",
                "display_name": "Existing User",
                "created_at": datetime.now(UTC),
            }
        ]

    def create_profile(self, email: str | None, display_name: str | None):
        return {
            "id": str(uuid4()),
            "email": email,
            "display_name": display_name,
            "created_at": datetime.now(UTC),
        }


def test_profile_create_valid_payload() -> None:
    payload = ProfileCreate(email="new@example.com", display_name="New User")
    assert payload.email == "new@example.com"
    assert payload.display_name == "New User"


def test_profile_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        ProfileCreate(email="not-an-email", display_name="User")


def test_profiles_service_list_profiles() -> None:
    service = ProfilesService(repository=StubProfilesRepository())
    result = service.list_profiles()

    assert len(result.items) == 1
    assert result.items[0].email == "existing@example.com"
    assert isinstance(result.items[0], ProfileRead)


def test_profiles_service_create_profile() -> None:
    service = ProfilesService(repository=StubProfilesRepository())
    payload = ProfileCreate(email="new@example.com", display_name="New User")
    result = service.create_profile(payload)

    assert result.email == "new@example.com"
    assert result.display_name == "New User"
    assert isinstance(result, ProfileRead)


def test_openapi_has_patch_profile_me_request_body_schema() -> None:
    openapi = app.openapi()
    profile_patch = openapi["paths"]["/profiles/me"]["patch"]

    assert "requestBody" in profile_patch
    assert profile_patch["requestBody"]["required"] is True
