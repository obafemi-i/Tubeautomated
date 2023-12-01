from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from crud.user import get_all_users, get_by_email, create_user, get_db
from security.hashing import verify_password
from security.tokens import create_access_token

from schemas.schema import UserCreate, UserResponse
from models.model import User


router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post('/create', response_model=UserResponse, response_description='Create a new user.', status_code=status.HTTP_201_CREATED)
def create(request: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(obj=request, db=db)
        return user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User with the email {request.email} already exists')


@router.get('/users', response_model=list[UserResponse], response_description='Retrieve all users, Admin only.', status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users


@router.get('/user/{email}', response_description='Get a user by their email.', response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_by_email(email=email, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'No user with email {email}')
    
    return user


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            details='Invalid login details')
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            details='Invalid login details')
    
    access_token = create_access_token(data={'sub': user.email, 'name': user.first_name})
    return {'access_token': access_token, 'token_type': 'bearer'}

