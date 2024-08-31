from starlette import status

from app.exceptions.base import BaseCustomException

class UnauthorizedException(BaseCustomException):
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ExpiredTokenException(BaseCustomException):
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenException(BaseCustomException):
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN
        )