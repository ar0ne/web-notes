from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, status_code: int = 404, detail: str = "Not found"):
        super().__init__(status_code, detail)
