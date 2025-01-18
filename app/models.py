from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


# Database model
class CallState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(index=True)
    status: str = Field(index=True)
    transcript: Optional[str] = Field(default=None, nullable=True)
    translation: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    duration: Optional[int] = Field(default=None, nullable=True, ge=0)
    caller_id: Optional[str] = Field(default=None, nullable=True, index=True)
    recording_url: Optional[str] = Field(default=None, nullable=True)
    user_id: Optional[int] = Field(default=None, nullable=True, index=True)
    user_role: Optional[str] = Field(default=None, nullable=True)


# User model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: Optional[str] = Field(default=None, nullable=True, index=True)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None, nullable=True)
    disabled: Optional[bool] = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
