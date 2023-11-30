from pydantic import BaseModel, validator, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr = Field(examples=['tube@automated.com'])
    password: str
    first_name: str = Field(examples=['Mufasa'])


class UserResponse(BaseModel):
    email: str
    first_name: str

    class config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    first_name: str | None = None

