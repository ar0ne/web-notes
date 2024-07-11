from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from src.note.models import NoteCollection

mongodb_url = "mongodb://user:pass@localhost:27017/app?retryWrites=true&w=majority&authSource=admin"

client = AsyncIOMotorClient(mongodb_url)
db = client.app
note_collection = db.get_collection("notes")


async def get_notes():
    return NoteCollection(notes=await note_collection.find().to_list(1000))


async def get_note(id: str):
    return await note_collection.find_one({"_id": ObjectId(id)})
