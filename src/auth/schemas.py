from datetime import datetime
from enum import Enum, unique
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


@unique
class UserOnlineStatus(str, Enum):
    online = 'online'
    offline = 'offline'
    sleeping = 'sleeping'


class UserChangePassword(UserBase):
    old_password: str
    new_password: str


class UserChange(UserCreate):
    is_superuser: bool | None
    is_admin: bool | None
    last_activity: datetime | None
    is_online: bool | None
    online_status: UserOnlineStatus | None


class User(UserBase):
    id: int
    hashed_password: str
    is_superuser: bool | None
    is_admin: bool | None
    registration_date: datetime | None
    last_activity: datetime | None
    is_online: bool | None
    online_status: UserOnlineStatus | None

    class Config:
        orm_mode = True
