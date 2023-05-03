from typing_extensions import Annotated
from fastapi import Body
from fastapi.routing import APIRouter
from src.auth.dependencies import GetCurrentUserDep, PaginationDep
from src.database import SessionLocal
from src.chat import schemas
from src.chat import models


router = APIRouter(
    prefix='/chats',
    tags=['chats'],
    dependencies=None,
    responses=None
)


@router.get('', response_model=list[schemas.Chat])
def get_chats(current_user: GetCurrentUserDep, pagination: PaginationDep):
    with SessionLocal() as db:
        chats_db = db.query(models.Chat).offset(
            pagination["skip"]).limit(pagination["limit"]).all()
        return chats_db


@router.post('/', response_model=schemas.Chat)
def create_chat(current_user: GetCurrentUserDep, chat: Annotated[schemas.ChatCreate, Body()]):
    with SessionLocal() as db:
        chat_db = models.Chat(title=chat.title)
        db.add(chat_db)
        db.commit()
        user_chat_db = models.UserChatRel(
            user_id=current_user.id, chat_id=chat_db.id)
        db.add(user_chat_db)
        db.commit()
        db.refresh(chat_db)
        return chat_db


@router.post('/send/', response_model=schemas.Message)
def send_message(current_user: GetCurrentUserDep, message_send: Annotated[schemas.MessageSend, Body()]):
    with SessionLocal() as db:

        # Check if user_chat_rel exists

        # db.query(models.UserChatRel).filter(models.UserChatRel.user)

        message_db = models.Message(
            text=message_send.text, chat_id=message_send.chat_id)
        db.add(message_db)
        db.commit()
        db.refresh(message_db)
        return message_db
