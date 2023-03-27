from pydantic import BaseModel
from ..auth.schemas import User


class Chat(BaseModel):
    id: int
    title: str


class Message(BaseModel):
    id: int
    chat: Chat
