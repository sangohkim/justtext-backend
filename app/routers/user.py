from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, auth, schemas
from ..database import get_db

from datetime import datetime, timedelta
from typing import List
import pytz


router = APIRouter()


@router.post('/user/register', response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    if db_user:
        # 탈퇴했던 유저가 재가입하는 경우
        if db_user.deleted_at:
            setattr(db_user, "deleted_at", None)
            db.commit()
            db.refresh(db_user)
            return db_user

        # 그 외의 경우
        raise HTTPException(status_code=400, detail="name already exists")
    hashed_password = auth.get_password_hash(user.pw)
    db_user = models.User(name=user.name, pw=hashed_password, created_at=datetime.now(pytz.UTC))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/user/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_name": user.name}


# fastapi가 /user/me, /user/{user_id}를 헷갈릴 수 있음. me가 더 위로 오도록 변경해야 함.
@router.get("/user/me", response_model=schemas.User)
def get_my_info(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@router.get("/user/my-posts")
def get_my_all_posts(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # soft delete 된 문서는 제외
    db_posts = db.query(models.Post).filter(models.Post.deleted_at.is_(None) == True, models.Post.user_id == current_user.id).all()
    return db_posts


@router.patch("/user/withdraw")
def withdraw_me(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    setattr(db_user, "deleted_at", datetime.now(pytz.UTC))
    db.commit()
    
    return {}


@router.get("/user/{user_id}", response_model=schemas.User)
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    # soft delete (탙퇴처리) 된 유저는 제외
    user = db.query(models.User).filter(models.User.deleted_at.is_(None) == True, models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user_id")
    
    return user
