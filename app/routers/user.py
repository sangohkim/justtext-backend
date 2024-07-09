from fastapi import APIRouter


router = APIRouter()

@router.post('/user/register')
def register_user():
    ...


@router.post('/user/login')
def login():
    ...

@router.post('/user/logout')
def logout():
    ...