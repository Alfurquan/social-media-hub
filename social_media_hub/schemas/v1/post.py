from pydantic import BaseModel, Field, HttpUrl
from annotated_types import Len
from typing import Annotated, List
from .like import Like

class ImageBase(BaseModel):
    path: str
    file_name: str
    
class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id : int

class PostBase(BaseModel):
    title: Annotated[str, Len(min_length=1), Len(max_length=50)]
    description: Annotated[str, Len(min_length=1), Len(max_length=255)]
    
class PostCreate(PostBase):
    images: List[ImageCreate] = []

class PostUpdate(BaseModel):
    title: Annotated[str | None, Len(min_length=1), Len(max_length=50)] = None
    description: Annotated[str | None, Len(min_length=1), Len(max_length=255)] = None

class Post(PostBase):
    id: int
    author_id: int
    likes: List[Like] = Field(default_factory=list)
    images: List[Image] | None = None