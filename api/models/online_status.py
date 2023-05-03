from typing import Optional, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.db.database import Base


class OnlineStatus(Base):
    __tablename__ = "online_status"

    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(length=18), nullable=False, unique=True)
    image_url: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=False)

    users = relationship("User", back_populates="online_status")
