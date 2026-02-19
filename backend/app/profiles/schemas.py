from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ProfileBase(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None


class ProfileCreate(ProfileBase):
    # If you are using the auth trigger, you may not need create at all,
    # but we keep it to satisfy existing router imports.
    pass


class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None


class ProfileRead(ProfileBase):
    id: str
    created_at: datetime


class ProfileListResponse(BaseModel):
    items: list[ProfileRead]