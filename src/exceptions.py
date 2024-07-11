from fastapi import HTTPException


class NotFoundException(HTTPException):
    status_code = 404
    detail = "Not found."
