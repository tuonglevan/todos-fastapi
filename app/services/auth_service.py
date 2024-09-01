from datetime import timedelta
from typing import Optional

from jose import jwt, JWTError
from app.exceptions.auth_exceptions import UnauthorizedException, ForbiddenException
from app.models import user as UserModel
from app.schemas.user import UserInToken
from .user_service import UserService
from app.utils.time_utils import get_current_utc_datetime

class AuthService:
    def __init__(self, config, user_service: UserService):
        self.config = config
        self.user_service = user_service

    async def authenticate_user(self, username: str, password: str) -> Optional[UserModel]:
        user = await self.user_service.fetch_user_by_username(username)
        if not user or not UserModel.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, user: UserModel, expires: Optional[timedelta] = None):
        claims = {
            "id": str(user.id),
            "sub": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin
        }
        expire = get_current_utc_datetime() + expires if expires else get_current_utc_datetime() + timedelta(minutes=15)
        claims.update({"exp": expire})
        return jwt.encode(claims, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)

    def decode_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.config.JWT_SECRET_KEY, algorithms=[self.config.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    def get_current_user(self, token: str) -> UserInToken:
        payload = self.decode_token(token)
        if payload is None:
            raise UnauthorizedException(detail="Invalid authentication credentials")
        user = UserInToken(**payload)
        return user

    @staticmethod
    def is_authenticated(user: UserInToken) -> UserInToken:
        if user is None:
            raise UnauthorizedException(detail="Not authenticated")
        return user

    @staticmethod
    def is_admin(user: UserInToken) -> UserInToken:
        if not user.is_admin:
            raise ForbiddenException(detail="Not an admin")
        return user