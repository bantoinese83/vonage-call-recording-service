import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlmodel import select

from app.database import async_session, CallState
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
async def clear_database():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(CallState))
            await session.commit()

@pytest.mark.asyncio
async def test_answer_call():
    response = client.post("/api/v1/calls/answer", params={"uuid": "test-uuid"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "action": "talk",
            "text": "This call will be recorded for quality assurance purposes.",
        },
        {
            "action": "record",
            "eventUrl": ["http://testserver/api/v1/calls/recordings"],
            "beepStart": False,
        },
        {
            "action": "connect",
            "endpoint": [
                {
                    "type": "phone",
                    "number": "16362145464",
                }
            ],
        },
    ]

    # Verify that the call state is stored in the database
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == "test-uuid"))
            call_state = result.scalar_one_or_none()
            assert call_state is not None
            assert call_state.status == "recording"

def test_answer_call_missing_uuid():
    response = client.post("/api/v1/calls/answer")
    assert response.status_code == 422  # Unprocessable Entity

def test_answer_call_invalid_uuid():
    response = client.post("/api/v1/calls/answer", params={"uuid": ""})
    assert response.status_code == 422  # Unprocessable Entity

@patch("app.services.transcribe_and_translate", return_value=None)
@pytest.mark.asyncio
async def test_handle_recording_event(mock_transcribe_and_translate):
    event_data = {
        "uuid": "test-uuid",
        "url": "http://testserver/recording.mp3",
        "status": "completed",
    }
    response = client.post("/api/v1/calls/recordings", json=event_data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_handle_call_event():
    event_data = {"uuid": "test-uuid", "status": "completed"}
    response = client.post("/api/v1/calls/events", json=event_data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Verify that the call state is deleted from the database
    async with async_session() as session:
        async with session.begin():
            call_state = await session.get(CallState, "test-uuid")
            assert call_state is None

@pytest.mark.asyncio
async def test_get_dashboard():
    response = client.get("/api/v1/dashboard/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_duration" in data
    assert "total_recordings" in data
    assert "success_rate" in data
    assert "average_duration" in data

@pytest.mark.asyncio
async def test_get_recordings():
    # First, get a token
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "johndoe", "password": "secret"},
    )
    token = response.json()["access_token"]

    # Use the token to access the protected route
    response = client.get(
        "/api/v1/recordings/list",
        params={"search": "test", "page": 1, "limit": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "recordings" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data

@patch("app.aws_setup.upload_file_to_s3", return_value="http://mock_s3_url/recording.mp3")
@pytest.mark.asyncio
async def test_create_recording(mock_upload_file_to_s3):
    with open("test_audio.wav", "wb") as f:
        f.write(b"test audio content")
    with open("test_audio.wav", "rb") as f:
        response = client.post(
            "/api/v1/recordings/create",
            files={"audio": f},
            data={"caller_id": "test-caller", "duration": 60},
        )
    os.remove("test_audio.wav")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "recording_id" in data

def test_login_for_access_token():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "johndoe", "password": "secret"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_for_access_token_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "johndoe", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }

@pytest.mark.asyncio
async def test_read_users_me():
    # First, get a token
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "johndoe", "password": "secret"},
    )
    token = response.json()["access_token"]

    # Use the token to access the protected route
    response = client.get(
        "/api/v1/auth/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "johndoe@example.com"
    assert data["full_name"] == "John Doe"
    assert data["disabled"] == False

@pytest.mark.asyncio
async def test_read_users_me_unauthorized():
    response = client.get("/api/v1/auth/user")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }