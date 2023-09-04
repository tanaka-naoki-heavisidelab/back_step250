import re
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from server.schemas.user import User, UserPost, UserCreate
from server.services.toUser import create, select_by_email
from server.services.toAuth import get_current_user, get_pwd_context
from server.schemas.token import TokenData
from server.schemas.common import UserRead
from server.models.user import User as UserModel
from server.db.database import database
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
            usercreate = UserCreate(
                email=user.email, username=user.username, password=hashed_password
            )
            return await create(usercreate)


@router.get("/user", response_model=UserRead)
async def get_user(current_user: TokenData = Depends(get_current_user)):
    query = select([UserModel]).where(UserModel.email == current_user.email)
    result = await database.fetch_one(query)
    return result
