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
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


refresh_token_scheme = OAuth2RefreshTokenBearer()


@router.post("/token_refresh", response_model=Token)
async def refresh_access_token(refresh_token: str = Depends(refresh_token_scheme)):
    logger.info("     3.refresh_access_token")
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
    response.set_cookie(key="access_token", value=new_access_token, httponly=True)
    return response
