from starlette import status

from app.exceptions.base import BaseCustomException

class UserNotFoundException(BaseCustomException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND
        )