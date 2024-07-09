from fastapi import APIRouter


router = APIRouter()

@router.post('/post')
def create_post():
    ...


@router.patch('/post/update/{post_id}')
def update_post():
    ...


@router.patch('/post/delete/{post_id}')
def delete_post():
    ...


@router.get('/post/{post_id}')
def get_post():
    ...
