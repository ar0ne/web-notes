from fastapi import APIRouter

from src.exceptions import NotFoundException
from src.note.models import NoteCollection, NoteModel
from src.note import service as note_service

router = APIRouter()


@router.get("", response_model=NoteCollection)
async def get_notes():
    """Get all notes"""
    return await note_service.get_notes()


@router.get("/:id", response_model=NoteModel)
async def get_note(id: str):
    if (note := await note_service.get_note(id)) is not None:
        return note

    raise NotFoundException
