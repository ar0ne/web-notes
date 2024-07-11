from fastapi import APIRouter, Body
from fastapi.responses import Response
from starlette import status

from src.exceptions import NotFoundException
from src.note.models import NoteCollection, NoteModel, UpdateNoteModel
from src.note import service as note_service

router = APIRouter()


@router.get(
    "/",
    response_description="List all notes",
    response_model=NoteCollection,
    response_model_by_alias=False,
)
async def get_notes():
    """Get all notes"""
    return await note_service.get_notes()


@router.get(
    "/{id}",
    response_description="Get a single note",
    response_model=NoteModel,
    response_model_by_alias=False,
)
async def get_note(id: str):
    if (note := await note_service.get_note(id)) is not None:
        return note
    raise NotFoundException(detail=f"Note '{id}' not found.")


@router.post(
    "/",
    response_description="Create a note",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteModel,
    response_model_by_alias=False,
)
async def create_note(note: NoteModel):
    return await note_service.create_note(note)


@router.delete("/{id}", response_description="Delete a note", response_model=NoteModel)
async def delete_note(id: str):
    if await note_service.delete_note(id) is True:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise NotFoundException(detail=f"Note '{id}' not found.")


@router.put(
    "/{id}",
    response_description="Update a note",
    response_model=NoteModel,
    response_model_by_alias=False,
)
async def update_note(id: str, note: UpdateNoteModel = Body(...)):
    if (updated_note := await note_service.update_note(id, note)) is not None:
        return updated_note
    raise NotFoundException(detail=f"Note {id} not found.")
