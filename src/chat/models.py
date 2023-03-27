from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship
import src.auth.models as auth_models
from ..database import Base


user_chat_rel = Table(
    "user_chat_rel",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id"), primary_key=True),
)


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    users: Mapped[List[auth_models.User]] = relationship(
        secondary=user_chat_rel, back_populates="chats"
    )

    messages = relationship("Message", back_populates="chat_id")


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    chat_id = Column(ForeignKey('chats.id'))

    chat = relationship("Chat", back_populates="messages")
