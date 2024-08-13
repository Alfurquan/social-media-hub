from sqlalchemy import ForeignKey, Column, Integer, String, Table
from sqlalchemy.orm import relationship

from ...database import Base

user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey("users.id"), primary_key=True),
    Column('following_id', Integer, ForeignKey("users.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    posts = relationship("Post", back_populates="author")
    following = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers'
    )