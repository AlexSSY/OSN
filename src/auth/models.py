from datetime import datetime
from typing import List
from typing_extensions import Literal
from sqlalchemy import Boolean, Column, TIMESTAMP, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from src.database import Base
from .schemas import UserOnlineStatus
from ..models import user_chat_rel


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    registration_date = Column(TIMESTAMP, default=datetime.utcnow)
    last_activity = Column(TIMESTAMP, default=datetime.utcnow)
    is_online = Column(Boolean, default=False)
    online_status = Column(
        Enum(UserOnlineStatus), default=UserOnlineStatus.online.value, nullable=False)

    chats = relationship("Chat", secondary=user_chat_rel,
                         back_populates="users")
