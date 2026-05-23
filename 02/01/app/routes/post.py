from fastapi import APIRouter
from app.models.post import PostRequest
from app.services.post import create_post
from app.services.post import get_post


router = APIRouter(

    prefix="/posts",

    tags=["posts"]
)


@router.post("")
def create(post_data: PostRequest):

    return create_post(post_data)


@router.get("")
def list_posts():

    return get_post()