from starlette import status

from app.exceptions.base import BaseCustomException

class CompanyNotFoundException(BaseCustomException):
    def __init__(self, detail: str = "Company not found"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND
        )