from fastapi import HTTPException, status


class BaseCustomException(HTTPException):
    def __init__(self, detail: str, status_code: int, headers: dict | None = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)