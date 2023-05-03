from sqlalchemy import Table, Column, ForeignKey
from .database import Base

user_chat_rel = Table(
    "user_chat_rel",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id"), primary_key=True),
)
