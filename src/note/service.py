from fastapi import Body
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pymongo import ReturnDocument

from src.note.models import NoteCollection, NoteModel, UpdateNoteModel

# TODO:
mongodb_url = "mongodb://user:pass@localhost:27017/app?retryWrites=true&w=majority&authSource=admin"

client = AsyncIOMotorClient(mongodb_url)
db = client.app
note_collection = db.get_collection("notes")


async def get_notes():
    return NoteCollection(notes=await note_collection.find().to_list(1000))


async def get_note(id: str):
    return await note_collection.find_one({"_id": ObjectId(id)})


async def create_note(note: NoteModel = Body(...)):
    """insert note record"""
    new_note = await note_collection.insert_one(
        note.model_dump(by_alias=True, exclude=["id"])
    )
    created_note = await note_collection.find_one({"_id": new_note.inserted_id})
    return created_note


async def delete_note(id: str) -> bool:
    """Delete note record"""
    delete_result = await note_collection.delete_one({"_id": ObjectId(id)})
    return delete_result.deleted_count == 1


async def update_note(id: str, note: UpdateNoteModel = Body(...)):
    note = {k: v for k, v in note.model_dump(by_alias=True).items() if v is not None}

    if len(note) >= 1:
        update_result = await note_collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": note}, return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result

    return await note_collection.find_one({"_id": ObjectId(id)})
