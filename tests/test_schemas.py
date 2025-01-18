import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, RecordingEvent, CallEvent, DashboardData, Recording

def test_user_create_model():
    user = UserCreate(
        username="testuser",
        password="testpassword",
        email="testuser@example.com",
        full_name="Test User"
    )
    assert user.username == "testuser"
    assert user.password == "testpassword"
    assert user.email == "testuser@example.com"
    assert user.full_name == "Test User"

def test_user_create_model_missing_fields():
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", password="testpassword")

def test_recording_event_model():
    event = RecordingEvent(
        url="http://testserver/recording.mp3",
        uuid="test-uuid",
        status="completed"
    )
    assert event.url == "http://testserver/recording.mp3"
    assert event.uuid == "test-uuid"
    assert event.status == "completed"

def test_call_event_model():
    event = CallEvent(
        uuid="test-uuid",
        status="completed"
    )
    assert event.uuid == "test-uuid"
    assert event.status == "completed"

def test_dashboard_data_model():
    data = DashboardData(
        total_duration=100,
        total_recordings=10,
        success_rate=90.0,
        average_duration=10.0
    )
    assert data.total_duration == 100
    assert data.total_recordings == 10
    assert data.success_rate == 90.0
    assert data.average_duration == 10.0

def test_recording_model():
    recording = Recording(
        id=1,
        date="2023-01-01T00:00:00",
        duration=60,
        caller_id="test-caller",
        status="completed",
        user_id=1,
        user_role="admin"
    )
    assert recording.id == 1
    assert recording.date == "2023-01-01T00:00:00"
    assert recording.duration == 60
    assert recording.caller_id == "test-caller"
    assert recording.status == "completed"
    assert recording.user_id == 1
    assert recording.user_role == "admin"
