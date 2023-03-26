from datetime import timedelta
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from sqlalchemy.orm import Session

from .utils import create_access_token, get_password_hash, verify_password
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import GetDBDep
from .schemas import UserBase, UserCreate, User, UserChange, Token
from .dependencies import GetCurrentUserDep, PaginationDep
from ..database import SessionLocal
from . import models

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=None,
    responses=None
)


@router.post('/', response_model=User)
def create_new_user(user: Annotated[UserCreate, Body()]):
    with SessionLocal() as db:
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(
                status_code=400, detail=f'User {user.email} is already exists')
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@router.get('', response_model=list[User])
def get_users(pagination: PaginationDep, db: GetDBDep, current_user: GetCurrentUserDep):
    return db.query(models.User).offset(pagination['skip']).limit(pagination['limit']).all()


@router.get('/me', response_model=User)
def get_me(current_user: GetCurrentUserDep):
    return current_user


@router.get('/{user_id}', response_model=User)
def get_user(user_id: Annotated[int, Path()], db: GetDBDep):
    db_user = db.query(models.User).get(user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=f'User with id: {user_id} not found')
    return db_user


@router.patch('/{user_id}/', response_model=User)
def change_user(user_id: Annotated[int, Path()], user: UserChange, current_user: GetCurrentUserDep):
    with SessionLocal() as db:
        db_user = db.get(models.User, user_id)
        key_val = user.dict(exclude_unset=True)

        if key_val.get('is_superuser') and not current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail='You no have rights to change superuser status')

        if key_val.get('is_admin') and not current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail='You no have rights to change admin status')

        for key, value in key_val.items():
            setattr(db_user, key, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


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
