from pydantic import BaseModel

class PostRequest(BaseModel):
    title:str
    content:str
    author:str

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    author:str

