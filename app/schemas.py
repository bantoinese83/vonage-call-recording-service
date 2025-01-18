from typing import Optional

from pydantic import BaseModel, HttpUrl, constr, conint, confloat, EmailStr


# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class RecordingEvent(BaseModel):
    url: HttpUrl
    uuid: constr(min_length=1)
    status: constr(min_length=1)


class CallEvent(BaseModel):
    uuid: constr(min_length=1)
    status: constr(min_length=1)


class DashboardData(BaseModel):
    total_duration: conint(ge=0)
    total_recordings: conint(ge=0)
    success_rate: confloat(ge=0, le=100)
    average_duration: confloat(ge=0)


class Recording(BaseModel):
    id: conint(ge=1)
    date: str
    duration: conint(ge=0)
    caller_id: Optional[constr(min_length=1)]
    status: constr(min_length=1)
    user_id: Optional[int]
    user_role: Optional[str]
