from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel

from starlette.responses import JSONResponse

from src.note.views import router as note_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

api_router.include_router(note_router, prefix="/notes", tags=["notes"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
