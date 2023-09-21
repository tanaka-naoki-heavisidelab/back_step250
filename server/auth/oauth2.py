from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from typing import Dict

# ロガーの設定
import logging

logging.basicConfig(level=logging.INFO)
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
        logger.info("     1.cookie before get_current_user")
        authorization: str = request.cookies.get("access_token")
        logger.info("     2.cookie:" + str(authorization))
        authorization = "Bearer " + authorization
        scheme, param = get_authorization_scheme_param(authorization)

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
        logger.info("     3.cookie before token_refresh")
        refresh_token: str = request.cookies.get("access_token")
        logger.info("     4.cookie:" + str(refresh_token))
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
