from typing import Optional
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from .schemas import TokenData
from ..config import ALGORITHM, SECRET_KEY
from . import models
from ..database import SessionLocal


def pagination(skip: int = 0, limit: int = 10) -> dict:
    return {
        'skip': skip,
        'limit': limit,
    }


PaginationDep = Annotated[dict, Depends(pagination)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth/")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Optional[models.User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    with SessionLocal() as db:
        user = db.query(models.User).filter(
            models.User.email == token_data.username).first()
        if user is None:
            raise credentials_exception
        return user


GetCurrentUserDep = Annotated[models.User, Depends(get_current_user)]


async def get_current_super_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


GetCurrentSuperUserDep = Annotated[models.User,
                                   Depends(get_current_super_user)]
