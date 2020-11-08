from sqlalchemy.orm import Session

from api.utils import security
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    user = models.User(
        username=user.username,
        email=user.email,
        password=security.get_password_hash(user.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter_by(username=username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if not user:
        return False

    if not security.verify_password(password, user.password):
        return False

    return user
