from app.db.user_db import user_db
from app.models.user import UserLogin

def login_user(user_data: UserLogin):
    for user in user_db:
        if (
            user["username"] == user_data.username
            and user["password"] == user_data.password
        ):
            return {"message": "로그인 성공", "username": user["username"]}
    return None


