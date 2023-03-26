from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import GetDBDep
from .schemas import UserCreate, User, UserChange
from .dependencies import PaginationDep
from . import crud

router = APIRouter(
    prefix='/users',
    tags=['user'],
    dependencies=None,
    responses=None
)


@router.post('/', response_model=User)
def create_new_user(user: Annotated[UserCreate, Body()], db: GetDBDep):
    if crud.get_user_by_email(db=db, email=user.email):
        raise HTTPException(
            status_code=400, detail=f'User {user.email} is already exists')
    return crud.create_user(db=db, user=user)


@router.get('', response_model=list[User])
def get_users(pagination: PaginationDep, db: GetDBDep):
    return crud.get_users(db=db, skip=pagination['skip'], limit=pagination['limit'])


@router.put('/{user_id}', response_model=User)
def change_user(user: UserChange, db: GetDBDep):
    return crud.change_user(db=db, user=user)
