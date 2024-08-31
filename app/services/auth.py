from datetime import timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_config
from app.exceptions.auth_exceptions import UnauthorizedException, ForbiddenException
from app.models import user as UserModel
from app.schemas.user import UserInToken
from app.services import user as UserService
from app.utils.time_utils import get_current_utc_datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

config = get_config()

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[UserModel]:
    user = await UserService.fetch_user_by_username(db, username)
    if not user or not UserModel.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(user: UserModel, expires: Optional[timedelta] = None):
    claims = {
        "id": str(user.id),
        "sub": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin
    }
    expire = get_current_utc_datetime() + expires if expires else get_current_utc_datetime() + timedelta(minutes=15)
    claims.update({"exp": expire})
    return jwt.encode(claims, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInToken:
    payload = decode_token(token)
    if payload is None:
        raise UnauthorizedException(detail="Invalid authentication credentials")
    user = UserInToken(**payload)
    return user

def is_authenticated(user: UserInToken = Depends(get_current_user)) -> UserInToken:
    if user is None:
        raise UnauthorizedException(detail="Not authenticated")
    return user

def is_admin(user: UserInToken = Depends(is_authenticated)) -> UserInToken:
    if not user.is_admin:
        raise ForbiddenException(detail="Not an admin")
    return user