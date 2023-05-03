from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        index=True)

    email: Mapped[str] = mapped_column(
        String(length=319),
        nullable=False,
        unique=True)

    password: Mapped[bytes] = mapped_column(
        String(length=60),
        nullable=False)

    registered: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.utcnow,
        nullable=False)

    last_activity: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.utcnow,
        nullable=False)

    online_status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column="online_status.id",
                   ondelete="CASCADE"))

    online_status = relationship(
        "OnlineStatus",
        back_populates="users")

    is_online: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=False)

    def __repr__(self) -> str:
        return f"{self.email} - {self.online_status.name}"
