from pydantic import BaseModel, EmailStr
from typing import List
from .post import Post

class UserBase(BaseModel):
    name: str
    email: EmailStr
    username: str
    
class UserWithIdAndName(BaseModel):
    id: int
    name: str
      
class UserCreate(UserBase):
    password: str
  
class User(UserBase):
    id: int
    posts: List[Post]
    followers: List[UserWithIdAndName]
    