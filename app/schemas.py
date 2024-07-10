# API 호출에 사용되는 부분 (json serializing, deserializing)

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str

# 회원가입에 사용
class UserCreate(UserBase):
    pw: str

# User 테이블의 정보
class User(UserBase):
    id: int
    name: str
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    is_anon: bool

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    likes: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_anon: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str

class TokenData(BaseModel):
    name: Optional[str] = None