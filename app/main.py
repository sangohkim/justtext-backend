from typing import Union

from fastapi import FastAPI, HTTPException
from app.routers import user, post

from .schemas import Error

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)

@app.get('/')
def tmp_root():
    raise HTTPException(400, detail="hello world")