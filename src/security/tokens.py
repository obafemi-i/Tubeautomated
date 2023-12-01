from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import dotenv_values

from schemas.schema import TokenData

config = dotenv_values()

SECRET_KEY = config['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print('payload be', payload)
        email: str = payload.get('sub')
        name: str = payload.get('name')

        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, first_name=name)

    except JWTError:
        raise credentials_exception
    
    return token_data

