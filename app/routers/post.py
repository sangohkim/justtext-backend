from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db
from datetime import datetime

import pytz


router = APIRouter()


@router.post('/post/write', response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if len(post.title) == 0 or len(post.content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid format")
    db_post = models.Post(**post.model_dump(), user_id=current_user.id, created_at=datetime.now(pytz.UTC))
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch('/post/update/{post_id}', response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # soft delete를 고려
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == current_user.id, models.Post.deleted_at.is_(None) == True).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found. Invalid post_id")
    if len(db_post.title) == 0 or len(db_post.content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invaild format")
    for key, value in post.model_dump().items():
        setattr(db_post, key, value)
    db_post.updated_at = datetime.now(pytz.UTC)
    db.commit()
    db.refresh(db_post)
    return db_post


# Soft delete
@router.patch('/post/delete/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.deleted_at.is_(None) == True, models.Post.id == post_id, models.Post.user_id == current_user.id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.deleted_at = datetime.now(pytz.UTC)
    db.commit()
    return {}


@router.get('/post/{post_id}', response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    # soft delete 고려
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.deleted_at.is_(None) == True).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
