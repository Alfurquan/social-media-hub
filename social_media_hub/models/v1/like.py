from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from ...database import Base

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="likes")