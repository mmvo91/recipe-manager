from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from api.config import config
from api.features.users.services import authenticate_user
from api.features.users.schemas import UserLogin
from api.utils import security
from api.utils.db import get_db
from . import schemas

token_router = APIRouter()


@token_router.post("/token", response_model=schemas.Token)
def login_for_access_token(
        response: Response, form_data: UserLogin, db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.username, expires_delta=access_token_expires
    )

    response.set_cookie(key="access_token", value=f"Bearer {access_token}")

    return {"access_token": access_token, "token_type": "bearer"}
