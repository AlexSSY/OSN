from datetime import timedelta
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from sqlalchemy.orm import Session

from src.auth.utils import create_access_token, verify_password
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import GetDBDep
from .schemas import UserBase, UserCreate, User, UserChange, Token
from .dependencies import GetCurrentUserDep, PaginationDep
from ..database import SessionLocal
from . import crud, models

router = APIRouter(
    prefix='/users',
    tags=['users'],
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
def get_users(pagination: PaginationDep, db: GetDBDep, current_user: GetCurrentUserDep):
    return crud.get_users(db=db, skip=pagination['skip'], limit=pagination['limit'])


@router.get('/me', response_model=User)
def get_me(current_user: GetCurrentUserDep):
    return current_user


@router.get('/{user_id}', response_model=User)
def get_user(user_id: Annotated[int, Path()], db: GetDBDep):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=f'User with id: {user_id} not found')
    return db_user


@router.patch('/{user_id}/', response_model=User)
def change_user(user_id: Annotated[int, Path()], user: UserChange, db: GetDBDep):
    return crud.change_user(db=db, user=user)


@router.delete('/{user_id}/')
def delete_user(user_id: int):
    with SessionLocal() as db:
        user_db = db.get(models.User, user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail='user not found')
        db.delete(user_db)
        db.commit()
    return {'message': f'user with id: {user_id} deleted!'}


@router.post('/auth/', response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    with SessionLocal() as db:
        user = db.query(models.User).filter(
            models.User.email == form_data.username).first()
        if not user:
            raise exception
        if not verify_password(form_data.password, user.hashed_password):
            raise exception
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
