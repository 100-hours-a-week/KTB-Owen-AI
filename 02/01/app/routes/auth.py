from fastapi import APIRouter
from fastapi import HTTPException

from app.models.user import UserLogin
from app.services.auth import login_user


router = APIRouter()


@router.post("/login")
def login(user_data: UserLogin):

    result = login_user(user_data)

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    return result