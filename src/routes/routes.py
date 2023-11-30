from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud.user import get_all_users, get_by_email, create_user, get_db
from security.hashing import verify_password

from schemas.schema import UserCreate, UserResponse


router = APIRouter()


@router.get('/')
def read_root():
    return 'Server is running..'


@router.post('/create', response_model=UserResponse, response_description='Create a new user')
def create(request: UserCreate, db: Session = Depends(get_db)):
    user = create_user(obj=request, db=db)
    return user

