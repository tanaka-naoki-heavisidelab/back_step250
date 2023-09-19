from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from typing import Dict
import logging

# ロガーの設定
logger = logging.getLogger(__name__)


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        logger.info("OAuth2PasswordBearerWithCookie called")  # この行を追加
        authorization: str = request.cookies.get(
            "access_token"
        )  # changed to accept access token from httpOnly Cookie
        authorization = "Bearer " + authorization
        logger.info("access_token is " + str(authorization))

        scheme, param = get_authorization_scheme_param(authorization)
        logger.info("scheme is " + str(scheme))
        logger.info("param is " + str(param))
        logger.info("scheme and param is gotten!")

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class OAuth2RefreshTokenBearer(OAuth2):
    def __call__(self, request: Request) -> Optional[str]:
        refresh_token: str = request.cookies.get("refresh_token")
        if not refresh_token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return refresh_token
