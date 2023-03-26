from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserBase, UserChange
from .utils import get_password_hash


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def change_user(db: Session, user: UserChange) -> User:
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=404, detail=f'User: {user.email} not found')
    if user.is_superuser:
        db_user.is_superuser = user.is_superuser
    if user.is_admin:
        db_user.is_admin = user.is_admin
    if user.last_activity:
        db_user.last_activity = user.last_activity
