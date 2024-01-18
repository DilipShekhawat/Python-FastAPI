from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    # rating:Optional[int]=None

class CreatePost(Post):
    pass
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    name:str
    created_at:datetime

    class Config:
        orm_mode=True
               
class PostResponse(Post):
    id:int
    created_at:datetime
    user_id:int
    user:UserResponse

    class Config:
        orm_mode=True
class PostVoteResponse(BaseModel):
    Post:PostResponse
    votes:int
    
    class Config:
        orm_mode=True

class User(BaseModel):
    email:EmailStr
    name:str
    password:str

class CreateUser(User):
    pass

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
