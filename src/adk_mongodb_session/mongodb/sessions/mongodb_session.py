from typing import Annotated

from bson.objectid import ObjectId
from google.adk.sessions import Session
from pydantic import BeforeValidator, Field


def is_object_id(v: str) -> bool:
    try:
        ObjectId(v)
        return v
    except Exception:
        return False


PyObjectId = Annotated[
    str,
    BeforeValidator(is_object_id),
]


class MongodbSession(Session):
    """A session object that is managed by the MongodbSessionService."""

    id: PyObjectId = Field(alias="_id", default_factory=lambda: str(ObjectId()))
