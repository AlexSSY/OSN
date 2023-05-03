from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserChangePassword(UserCreate):
    new_password: str


class UserRetrieve(UserBase):
    id: int
    registered: datetime
    last_activity: datetime
    is_online: bool
    online_status: str

    class Config:
        orm_mode = True