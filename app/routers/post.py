from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db
from datetime import datetime


router = APIRouter()

@router.post('/post')
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = models.Post(**post.dict(), user_id=current_user.id, created_at=datetime.utcnow())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch('/post/update/{post_id}')
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == current_user.id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found or you don't have permission")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db_post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch('/post/delete/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == current_user.id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found or you don't have permission")
    db_post.deleted_at = datetime.utcnow()
    db.commit()
    return {"detail": "Post deleted"}


@router.get('/post/{post_id}')
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
