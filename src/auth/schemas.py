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


class UserChange(BaseModel):
    is_superuser: bool | None
    is_admin: bool | None
    last_activity: datetime | None
    is_online: bool | None
    online_status: UserOnlineStatus | None


class User(UserBase):
    id: int
    is_superuser: bool
    is_admin: bool
    registration_date: datetime
    last_activity: datetime
    is_online: bool
    online_status: UserOnlineStatus

    class Config:
        orm_mode = True


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
