from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.config import config
from api.features.tokens.schemas import TokenData
from api.features.users.models import User
from api.utils.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token", auto_error=False)


def get_current_user(
        db: Session = Depends(get_db),
        access_token: str = Cookie(None),
):
    from api.features.users.services import get_user_by_username

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except (JWTError, AttributeError):
        raise credentials_exception

    user = get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user
