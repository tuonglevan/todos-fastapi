from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.services import get_auth_service
from app.schemas.user import UserInToken
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
        auth_service: AuthService = Depends(get_auth_service),
        token: str = Depends(oauth2_scheme)
) -> UserInToken:
    return auth_service.get_current_user(token)

def is_authenticated(
        auth_service: AuthService = Depends(get_auth_service),
        user: UserInToken = Depends(get_current_user)
) -> UserInToken:
    return auth_service.is_authenticated(user)

def is_admin(
        auth_service: AuthService = Depends(get_auth_service),
        user: UserInToken = Depends(is_authenticated)
) -> UserInToken:
    return auth_service.is_admin(user)
