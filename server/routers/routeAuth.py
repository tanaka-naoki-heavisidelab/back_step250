from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security import OAuth2PasswordRequestForm
from server.auth.oauth2 import OAuth2RefreshTokenBearer
from fastapi.responses import JSONResponse
from server.schemas.token import Token
from datetime import datetime, timedelta

from server.services.toAuth import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

# ロガーの設定
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 720
router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    content = {"token_type": "bearer"}
    response = JSONResponse(content=content)
    logger.info("     1.start set_cookie at /token")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    logger.info("     2.set token:" + str(access_token))
    return response


refresh_token_scheme = OAuth2RefreshTokenBearer()


@router.post("/token_refresh", response_model=Token)
async def refresh_access_token(refresh_token: str = Depends(refresh_token_scheme)):
    user = await get_current_user(refresh_token)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    new_access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    content = {"token_type": "bearer"}
    response = JSONResponse(content=content)
    logger.info("     5.start token_refresh at /token")
    response.set_cookie(key="access_token", value=new_access_token, httponly=True)
    logger.info("     6.end token_refresh at /token")
    return response


# @router.post("/token_refresh", response_model=Token)
# async def refresh_access_token(refresh_token: str = Depends(refresh_token_scheme)):
#     user = await get_current_user(refresh_token)
#     if not user:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
#         )

#     # 新しいAccess Tokenを生成
#     new_access_token = create_access_token(
#         data={"sub": user.email},
#         expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
#     )

#     # Access Tokenの有効期限を計算
#     token_expiration = datetime.utcnow() + timedelta(
#         minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     content = {
#         "token_type": "bearer",
#         "expires_at": token_expiration.timestamp(),  # クライアントに有効期限を返す
#     }

#     response = JSONResponse(content=content)
#     response.set_cookie(key="access_token", value=new_access_token, httponly=True)
#     return response
