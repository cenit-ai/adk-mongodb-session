from typing import Annotated

from bson.objectid import ObjectId
from google.adk.sessions import Session
from pydantic import BeforeValidator, Field, PlainSerializer

# Custom type for MongoDB ObjectId
# Coerces incoming values to an ObjectId, and serializes to a string
PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(ObjectId),
    PlainSerializer(lambda x: str(x), return_type=str),
]


class MongodbSession(Session):
    """A session object that is managed by the MongodbSessionService."""

    pass
