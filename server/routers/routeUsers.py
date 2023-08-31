import re
from fastapi import APIRouter, Depends, HTTPException
from server.schemas.user import User, UserPost, UserCreate
from server.services.toUser import create, select_by_email
from server.services.toAuth import get_pwd_context
from passlib.context import CryptContext

router = APIRouter()
pwd_context = get_pwd_context()


@router.post("/register", response_model=User)
async def create_user(
    user: UserPost,
    pwd_context: CryptContext = Depends(get_pwd_context),
):
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if (
        user.username == ""
        or user.email == ""
        or user.password1 == ""
        or user.password2 == ""
    ):
        raise HTTPException(status_code=400, detail="空のフォームがあります")
    elif user.password1 != user.password2:
        raise HTTPException(status_code=422, detail="パスワードが一致しません")
    elif re.match(pattern, user.email) is None:
        raise HTTPException(status_code=422, detail="メールアドレスの形式になっていません")
    else:
        DBuser = await select_by_email(user.email)
        if DBuser != None:
            raise HTTPException(status_code=409, detail="登録済みです")
        else:
            hashed_password = pwd_context.hash(user.password1)
            us = UserCreate(
                email=user.email, username=user.username, password=hashed_password
            )
            return await create(us)
