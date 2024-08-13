from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from ..schemas.v1.user import User,UserCreate
from ..dependencies import get_db
from ..services import user as user_service
from .auth import oauth2_scheme
from ..utils.auth_utils import decode_token

router_v1 = APIRouter()

@router_v1.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, user.email)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    existing_user = user_service.get_user_by_username(db, user.username)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already registered")
     
    return user_service.create_user(db=db, user=user)

@router_v1.post("/{user_id}/follow", response_model=User)
def follow_user(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, db: Session = Depends(get_db)):
    my_user_id = decode_token(token)
    
    user = user_service.get_user_by_id(db, user_id)
    
    if my_user_id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not present")
    
    return user_service.follow_user(db, user_id, my_user_id)

@router_v1.post("/{user_id}/unfollow", response_model=User)
def unfollow_user(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, db: Session = Depends(get_db)):
    my_user_id = decode_token(token)
    
    user = user_service.get_user_by_id(db, user_id)
    
    if my_user_id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not present")
    
    return user_service.unfollow_user(db, user_id, my_user_id)
    
@router_v1.get("/me", response_model=User)
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user_id = decode_token(token)
    user = user_service.get_user_by_id(db, user_id)
    return user