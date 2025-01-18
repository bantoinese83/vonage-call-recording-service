import pytest
from app.models import CallState, User
from datetime import datetime, timezone

def test_call_state_model():
    call_state = CallState(
        id=1,
        uuid="test-uuid",
        status="completed",
        transcript="test transcript",
        translation="test translation",
        created_at=datetime.now(timezone.utc),
        duration=60,
        caller_id="test-caller",
        recording_url="http://testserver/recording.mp3",
        user_id=1,
        user_role="admin"
    )

    assert call_state.id == 1
    assert call_state.uuid == "test-uuid"
    assert call_state.status == "completed"
    assert call_state.transcript == "test transcript"
    assert call_state.translation == "test translation"
    assert call_state.duration == 60
    assert call_state.caller_id == "test-caller"
    assert call_state.recording_url == "http://testserver/recording.mp3"
    assert call_state.user_id == 1
    assert call_state.user_role == "admin"

def test_user_model():
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
        full_name="Test User",
        disabled=False,
        created_at=datetime.now(timezone.utc)
    )

    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.hashed_password == "hashedpassword"
    assert user.full_name == "Test User"
    assert user.disabled == False
