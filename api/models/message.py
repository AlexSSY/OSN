from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.database import Base


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    readed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey(column="user.id"))
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey(column="user.id"))

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])