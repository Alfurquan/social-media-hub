from sqlalchemy import ForeignKey, Column, Integer, String, Table
from sqlalchemy.orm import relationship

from ...database import Base

post_images = Table('post_images', Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    path = Column(String)
    post = relationship("Post", secondary=post_images, back_populates="images")