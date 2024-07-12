from fastapi import APIRouter, Body, Depends
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status

from src.database import get_database
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
async def get_notes(db: AsyncIOMotorClient = Depends(get_database)):
    """Get all notes"""
    return await note_service.get_notes(db)


@router.get(
    "/{note_id}",
    response_description="Get a single note",
    response_model=NoteModel,
    response_model_by_alias=False,
)
async def get_note(note_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    """Get single note by id"""
    if (note := await note_service.get_note(db, note_id)) is not None:
        return note
    raise NotFoundException(detail=f"Note '{note_id}' not found.")


@router.post(
    "/",
    response_description="Create a note",
    status_code=status.HTTP_201_CREATED,
    response_model=NoteModel,
    response_model_by_alias=False,
)
async def create_note(note: NoteModel, db: AsyncIOMotorClient = Depends(get_database)):
    """Create a note"""
    return await note_service.create_note(db, note)


@router.delete(
    "/{note_id}", response_description="Delete a note", response_model=NoteModel
)
async def delete_note(note_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    """Delete note by id"""
    if await note_service.delete_note(db, note_id) is True:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise NotFoundException(detail=f"Note '{note_id}' not found.")


@router.put(
    "/{note_id}",
    response_description="Update a note",
    response_model=NoteModel,
    response_model_by_alias=False,
)
async def update_note(
    note_id: str,
    note: UpdateNoteModel = Body(...),
    db: AsyncIOMotorClient = Depends(get_database),
):
    """Update a note"""
    if (updated_note := await note_service.update_note(db, note_id, note)) is not None:
        return updated_note
    raise NotFoundException(detail=f"Note {note_id} not found.")
