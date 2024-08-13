from sqlalchemy.orm import Session
from typing import List
from ..schemas.v1.post import PostCreate, PostUpdate, Image
from ..models.v1.post import Post
from ..models.v1.like import Like
from ..models.v1.image import Image
from ..utils.image_utils import handle_file_deletion

def create_post(db: Session, post: PostCreate, userid: int):
    db_post = Post(**post.model_dump(exclude='images'), author_id=userid)
    insert_images(db, post.images, db_post)
    db.refresh(db_post)
    return db_post

def insert_images(db: Session, images: List[Image], post: Post):
    for image in images:
        img = Image(file_name=image.file_name, path=image.path)
        db.add(img)
        db.commit()
        db.refresh(img)
        post.images.append(img)
        db.add(post)
        db.commit()
        
def get_posts_for_user(db: Session, userid: int):
    db_posts = db.query(Post).filter(Post.author_id == userid)
    return db_posts

def get_posts(db: Session):
    return db.query(Post).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, stored_post: Post, post_to_update: PostUpdate):
    update_data = post_to_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stored_post, key, value)
    
    db.commit()
    return stored_post

def delete_post(db: Session, stored_post: Post):    
    images = stored_post.images
    delete_images(db, images)
    db.delete(stored_post)
    db.commit()
    
def delete_images(db: Session, images: List[Image]):
    for image in images:
        db.delete(image)
        handle_file_deletion(image.path)
    db.commit()
        

def like_post(db: Session, post_id: int, user_id: int):
    like = db.query(Like).filter(Like.post_id == post_id,Like.user_id == user_id).first()
    post = get_post_by_id(db, post_id)
    
    if like:
        return post
    
    like_object = Like(user_id=user_id, post_id=post_id)
    db.add(like_object)
    db.commit()
    db.refresh(like_object)
    return post
    