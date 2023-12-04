from pydantic import BaseModel, Field, EmailStr

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


class VideoAdd(BaseModel):
    youtuber_email: str 
    video_description: str
    video_title: str
    video_category_id: str


class Video:
    def __init__(self, youtuber_email: str, video_description: str, video_title: str, video_category_id: str):
        self.youtuber_email = youtuber_email
        self.video_description = video_description
        self.video_title = video_title
        self.video_category_id = video_category_id