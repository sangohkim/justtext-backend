from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str


class UserAuth(UserBase):
    pw: str


class User(UserBase):
    id: int
    

class Error(BaseModel):
    message: str