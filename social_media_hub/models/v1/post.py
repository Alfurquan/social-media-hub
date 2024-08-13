from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from .image import post_images
from ...database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    
    title = Column(String, nullable=False)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    images = relationship("Image", secondary=post_images, back_populates="post")
    likes = relationship("Like", back_populates="post")