from fastapi import Body
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ReturnDocument

from src import config
from src.note.models import NoteCollection, NoteModel, UpdateNoteModel


def get_collection(db) -> AsyncIOMotorCollection:
    return db.get_database(config.MONGODB_DATABASE).get_collection(
        config.MONGODB_NOTE_COLLECTION
    )


async def get_notes(conn) -> NoteCollection:
    return NoteCollection(notes=await get_collection(conn).find().to_list(1000))


async def get_note(conn: AsyncIOMotorClient, id: str):
    return await get_collection(conn).find_one({"_id": ObjectId(id)})


async def create_note(conn: AsyncIOMotorClient, note: NoteModel = Body(...)):
    """insert note record"""
    collection = get_collection(conn)
    new_note = await collection.insert_one(
        note.model_dump(by_alias=True, exclude={"id"})
    )
    created_note = await collection.find_one({"_id": new_note.inserted_id})
    return created_note


async def delete_note(conn: AsyncIOMotorClient, id: str) -> bool:
    """Delete note record"""
    delete_result = await get_collection(conn).delete_one({"_id": ObjectId(id)})
    return delete_result.deleted_count == 1


async def update_note(
    conn: AsyncIOMotorClient, id: str, note: UpdateNoteModel = Body(...)
):
    collection = get_collection(conn)
    note = {k: v for k, v in note.model_dump(by_alias=True).items() if v is not None}
    # if there's nothing to update, just return existing record
    if len(note) >= 1:
        update_result = await collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": note}, return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result

    return await collection.find_one({"_id": ObjectId(id)})
