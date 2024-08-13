from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.v1.user import User
from ..schemas.v1.user import UserCreate
from ..utils.auth_utils import hash_password, verify_password

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(**user.model_dump(exclude='password'), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def follow_user(db: Session, follow_user_id: int, user_id: int):
    user = get_user_by_id(db, user_id)
    follow_user = get_user_by_id(db, follow_user_id)
    
    user.following.append(follow_user)
    db.commit()
    db.refresh(user)
    return user

def unfollow_user(db: Session, follow_user_id: int, user_id: int):
    user = get_user_by_id(db, user_id)
    follow_user = get_user_by_id(db, follow_user_id)
    
    if not follow_user in user.following:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not followed")
    
    user.following.remove(follow_user)
    db.commit()
    db.refresh(user)
    return user
    