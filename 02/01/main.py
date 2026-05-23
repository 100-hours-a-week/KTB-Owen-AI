from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.post import router as post_router


app = FastAPI(
    title="ch02",
    description="FastAPI 과제",
    version="0.0.1",
    docs_url="/swagger" # 등등의 메타정보와 기본설정 입력 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ],
    allow_credentials=True, # 쿠키 세션 허용 
    allow_methods=["*"], # GET,POST,PUT,DELETE 전부 허용
    allow_headers=["*"], # Authorization 등 헤더 허용 
)

app.include_router(auth_router)
app.include_router(post_router)

@app.get("/")
def main_page():
    return{
        "message":"mainpage"
    }
