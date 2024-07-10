# DB table을 object로

from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    pw = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, index=True)
    deleted_at = Column(TIMESTAMP)

    post = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = 'Post'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    likes = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, index=True)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    is_anon = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="post")
