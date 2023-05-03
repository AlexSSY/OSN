from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship
import src.auth.models as auth_models
from ..database import Base
from ..models import user_chat_rel


class UserChatRel(Base):
    __table__ = user_chat_rel


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    users: Mapped[List[auth_models.User]] = relationship(
        secondary=user_chat_rel, back_populates="chats"
    )

    messages = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    chat_id = Column(ForeignKey('chats.id'))

    chat = relationship("Chat", back_populates="messages")
