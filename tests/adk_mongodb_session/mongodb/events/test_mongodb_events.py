import asyncio
import unittest
from unittest.mock import patch

from bson import ObjectId
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions
from google.adk.sessions.state import State
from google.genai.types import Content, Part
from mongomock import MongoClient

from src.adk_mongodb_session.mongodb.sessions.mongodb_session_service import (
    MongodbSessionService,
)


class TestMongodbEventsSessions(unittest.TestCase):
    def setUp(self):
        self.db_url = "mongodb://localhost:27017/"
        self.database = "test_db"
        self.collection_prefix = "test"
        self.app_name = "test_app"
        self.user_id = "test_user"
        self.session_id = ObjectId()

    @patch(
        "src.adk_mongodb_session.mongodb.sessions.mongodb_session_service.MongoClient",
        new=MongoClient,
    )
    def test_session_events(self):
        service = MongodbSessionService(
            db_url=self.db_url,
            database=self.database,
            collection_prefix=self.collection_prefix,
        )

        async def run_test():
            # 1. Create a session with tiered state
            initial_state = {
                f"{State.APP_PREFIX}app_key": "app_value",
                f"{State.USER_PREFIX}user_key": "user_value",
                "session_key": "session_value",
            }
            session = await service.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=str(self.session_id),
                state=initial_state,
            )

            # 2. Append an event to the session
            event = Event(
                invocation_id="test_invocation_id",
                author="test_author",
                actions=EventActions(state_delta={"session_key": "session_value_2"}),
                content=Content(parts=[Part(text="test_content")]),
            )
            await service.append_event(session, event)

            # 3. Get the session and verify the event was appended
            retrieved_session = await service.get_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=str(self.session_id),
            )
            self.assertEqual(1, len(retrieved_session.events))
            self.assertEqual(
                "session_value_2",
                retrieved_session.events[0].actions.state_delta["session_key"],
            )

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
