import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from server.auth.oauth2 import OAuth2PasswordBearerWithCookie
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from server.schemas.token import TokenData
from server.db.database import database
from server.models.user import User as UserModel
import logging

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


# Dependの引数にするには関数型で渡す。インスタンスはエラーになる。
def get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def verify_password(password, db_password):
    pwd_context = get_pwd_context()
    return pwd_context.verify(password, db_password)


async def get_user(email: str):
    query = select([UserModel]).where(UserModel.email == email)
    result = await database.fetch_one(query)
    return result


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")

#         if email is None:
#             raise credential_exception
#         token_data = TokenData(email=email)

#     except JWTError:
#         raise credential_exception

#     user = await get_user(email=token_data.email)
#     if user is None:
#         raise credential_exception
#     return user

# ログの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# logger インスタンスの作成
logger = logging.getLogger(__name__)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    logger.info("Entering get_current_user function")  # 関数が呼び出されたことを確認するためのログ

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        logger.info(f"Decoded JWT payload: {payload}")  # ペイロードの中身をログに出力

        if email is None:
            raise credential_exception
        token_data = TokenData(email=email)

    except JWTError:
        logger.error("JWT Error encountered while decoding token")  # エラーが発生した場合のログ
        raise credential_exception

    user = await get_user(email=token_data.email)
    if user is None:
        logger.warning(
            f"No user found with email: {token_data.email}"
        )  # 該当のユーザーが見つからない場合のログ
        raise credential_exception

    return user
