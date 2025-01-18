import os
import pytest
from fastapi.testclient import TestClient
from main import app
from app.auth import create_user, get_password_hash
from app.database import async_session
from app.models import User

client = TestClient(app)

@pytest.fixture(autouse=True)
async def clear_database():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(User))
            await session.commit()

@pytest.mark.asyncio
async def test_sign_up():
    response = client.post(
        "/api/v1/auth/signup",
        json={"username": "johndoe", "password": "secret", "email": "johndoe@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["email"] == "johndoe@example.com"

@pytest.mark.asyncio
async def test_login_for_access_token():
    # First, sign up a new user
    response = client.post(
        "/api/v1/auth/signup",
        json={"username": "johndoe", "password": "secret", "email": "johndoe@example.com"}
    )
    assert response.status_code == 200

    # Then, get a token
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "johndoe", "password": "secret"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_current_user():
    # First, sign up a new user
    response = client.post(
        "/api/v1/auth/signup",
        json={"username": "johndoe", "password": "secret", "email": "johndoe@example.com"}
    )
    assert response.status_code == 200

    # Then, get a token
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

@pytest.mark.asyncio
async def test_handle_call_event():
    event_data = {"uuid": "test-uuid", "status": "completed"}
    response = client.post("/api/v1/calls/events", json=event_data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_handle_recording_event():
    event_data = {
        "uuid": "test-uuid",
        "url": "http://testserver/recording.mp3",
        "status": "completed",
    }
    response = client.post("/api/v1/calls/recordings", json=event_data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_list_recordings():
    # First, sign up a new user
    response = client.post(
        "/api/v1/auth/signup",
        json={"username": "johndoe", "password": "secret", "email": "johndoe@example.com"}
    )
    assert response.status_code == 200

    # Then, get a token
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

@pytest.mark.asyncio
async def test_get_dashboard_data():
    response = client.get("/api/v1/dashboard/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_duration" in data
    assert "total_recordings" in data
    assert "success_rate" in data
    assert "average_duration" in data

@pytest.mark.asyncio
async def test_create_recording():
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
