from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.utils.db import get_db
from api.utils.security import get_current_active_user
from . import schemas, services

users_router = APIRouter()


@users_router.get(
    "/",
    response_model=List[schemas.User],
    dependencies=[Depends(get_current_active_user)],
)
def get_users(db: Session = Depends(get_db)):
    return services.get_users(db)


@users_router.post(
    "/",
    response_model=schemas.User
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db=db, user=user)


@users_router.get(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(get_current_active_user)],
)
def get_users(user_id: int, db: Session = Depends(get_db)):
    return services.get_user(db, user_id)
