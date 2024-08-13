from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Annotated, List
from ..schemas.v1.post import Post, PostCreate, PostUpdate, ImageCreate
from ..dependencies import get_db
from ..routers.auth import oauth2_scheme
from ..services import post as post_service
from ..utils.auth_utils import decode_token
from ..utils.image_utils import handle_file_upload

router_v1 = APIRouter()

@router_v1.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(token: Annotated[str, Depends(oauth2_scheme)], 
                title: str = Form(...),
                description: str = Form(...),
                images : List[UploadFile] = [], 
                db: Session = Depends(get_db)):
    
    user_id = decode_token(token)
    post_images: List[ImageCreate] = []
    
    for image in images:
        file_name = await handle_file_upload(image)
        post_images.append(ImageCreate(path=file_name, file_name=image.filename))
    
    post = PostCreate(title=title, description=description, images=post_images)
    return post_service.create_post(db, post, user_id)

@router_v1.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    
    return post_service.get_posts(db)

@router_v1.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post_by_id(db, post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    
    return post

@router_v1.patch("/{post_id}", response_model=Post)
def update_post(post_id: int, 
                token: Annotated[str, Depends(oauth2_scheme)],
                post_to_update: PostUpdate,
                db: Session = Depends(get_db)):
    
    user_id = decode_token(token)
    stored_post = post_service.get_post_by_id(db, post_id)
    
    if not stored_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    
    if stored_post.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not author of post")
    

    return post_service.update_post(db, stored_post, post_to_update)

@router_v1.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                token: Annotated[str, Depends(oauth2_scheme)],
                db: Session = Depends(get_db)):
    
    user_id = decode_token(token)
    stored_post = post_service.get_post_by_id(db, post_id)
    
    if not stored_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    
    if stored_post.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not author of post")
    
    post_service.delete_post(db, stored_post)
    

@router_v1.post("/{post_id}/likes", response_model=Post)
def like_post(post_id: int,
              token: Annotated[str, Depends(oauth2_scheme)],
              db: Session = Depends(get_db)):
    
    
    user_id = decode_token(token)
    stored_post = post_service.get_post_by_id(db, post_id)
    
    if not stored_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    
    return post_service.like_post(db, post_id, user_id)