# Plan for adk-mongodb-session

This plan outlines the steps taken to create a MongoDB session handler package similar to `google.adk.sessions`.

## 1. Project Structure

- [x] Create the directory structure: `src/adk/mongodb/sessions/`
- [x] Add `__init__.py` files to make the directories into Python packages.
- [x] Create the main session file: `src/adk/mongodb/sessions/mongodb_session.py`
- [x] Create the session service file: `src/adk/mongodb/sessions/mongodb_session_service.py`

## 2. Dependencies

- [x] Add `pymongo` as a dependency in `pyproject.toml`.
- [x] Add `mongomock` as an optional test dependency.
- [x] Install dependencies using `pip install -e ".[test]"`.

## 3. Core Implementation

- [x] **`MongodbSessionService` Class:** Implement a service class that inherits from `google.adk.sessions.base_session_service.BaseSessionService`.
- [x] **Connection Management:** The service's constructor takes MongoDB connection details (`db_url`, `database`, `collection_prefix`) and establishes a connection.
- [x] **Three-Tiered State Management:**
    - [x] Implement logic to manage three separate MongoDB collections for `app`, `user`, and `session` states.
    - [x] Replicate the state splitting (`_extract_state_delta`) and merging (`_merge_state`) logic from the reference `DatabaseSessionService`.
- [x] **Implement Abstract Methods:**
    - [x] `create_session`: Create session documents and manage state persistence across the three tiers.
    - [x] `get_session`: Retrieve a session and construct its state by merging app, user, and session data.
    - [x] `list_sessions`: List all sessions for a user, each with its correctly merged state.
    - [x] `delete_session`: Delete a session document from the database.
- [x] **`MongodbSession` Class:** Define a simple `pydantic` model inheriting from `google.adk.sessions.session.Session` to act as a data container, with no direct database logic.

## 4. Testing

- [x] Create a `tests/` directory with a parallel package structure.
- [x] Write unit tests for the `MongodbSessionService`.
- [x] Use `mongomock` to patch `MongoClient` and isolate tests from a live database.
- [x] Ensure all service methods (`create`, `get`, `list`, `delete`) and the state management logic are tested.

## 5. Packaging & Documentation

- [x] Update `pyproject.toml` with the correct package metadata and dependencies.
- [x] Add a `README.md` with installation instructions and usage examples.
- [ ] Build the package for distribution.