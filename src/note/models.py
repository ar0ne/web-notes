from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict

from src.models import PyObjectId


class NoteModel(BaseModel):
    """
    Container for a single note record.
    """

    # The primary key for the NoteModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    body: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Smart Idea",
                "body": "Here I describe my idea.",
            }
        },
    )


class UpdateNoteModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    title: str = Field(...)
    body: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Smart Idea",
                "body": "Here I describe my idea.",
            }
        },
    )


class NoteCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.
    """

    notes: List[NoteModel]
