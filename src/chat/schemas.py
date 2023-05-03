from typing_extensions import Literal
from pydantic import BaseModel
from ..auth.schemas import User


class ChatBase(BaseModel):
    title: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    # users: list[User]
    # messages: list[Literal["Message"]]

    class Config:
        orm_mode = True


class MessageSend(BaseModel):
    text: str
    user_id: int


class Message(BaseModel):
    id: int
    text: str
    chat_id: int
    # chat: Chat

    class Config:
        orm_mode = True
