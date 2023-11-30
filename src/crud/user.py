from fastapi import Depends
from sqlalchemy.orm import Session

from schemas.schema import UserCreate, UserResponse
from models.model import User
from security.hashing import get_password_hash
from models.database import Base, sessionLocal, engine

Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_user(obj: UserCreate, db: Session) -> UserResponse:
    hashed_password = get_password_hash(obj.password)
    new_obj = User(
        email = obj.email,
        password = hashed_password,
        first_name = obj.first_name
    )

    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


def get_by_email(db: Session, email: str) -> UserResponse | None:
    user = db.query(User).filter(User.email == email).first()
    return user


def get_all_users(db: Session) -> list[UserResponse]:
    users = db.query(User).all()
    return users

