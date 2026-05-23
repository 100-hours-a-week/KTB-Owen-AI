from app.db.post_db import post_db

from app.models.post import PostResponse
from app.models.post import PostRequest

def create_post(post_data: PostRequest):
    post = PostResponse(
        id=len(post_db) + 1,
        title=post_data.title,
        content=post_data.content,
        author=post_data.author,
    )
    post_db.append(post)
    return post 

def get_post():
    return post_db

