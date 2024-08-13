from .models.v1 import image, like, post
from .database import SessionLocal

from .database import SessionLocal, engine
from .models.v1 import user

user.Base.metadata.create_all(bind=engine)
post.Base.metadata.create_all(bind=engine)
like.Base.metadata.create_all(bind=engine)
image.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()