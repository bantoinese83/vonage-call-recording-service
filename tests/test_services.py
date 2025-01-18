import pytest
from unittest.mock import patch, AsyncMock
from app.services import (
    store_call_state,
    handle_recording,
    handle_call_event_service,
    get_dashboard_data,
    get_recordings_data,
    create_new_recording,
)
from app.enums import CallStatus
from app.schemas import DashboardData, Recording
from app.crud import create_call_state, get_call_state, delete_call_state, get_all_call_states, search_call_states, create_recording_file

@pytest.mark.asyncio
async def test_store_call_state():
    call_uuid = "test-uuid"
    await store_call_state(call_uuid)
    call_state = await get_call_state(call_uuid)
    assert call_state is not None
    assert call_state.uuid == call_uuid
    assert call_state.status == CallStatus.RECORDING.value

@pytest.mark.asyncio
@patch("app.services.transcribe_and_translate", new_callable=AsyncMock)
async def test_handle_recording(mock_transcribe_and_translate):
    call_uuid = "test-uuid"
    recording_url = "http://testserver/recording.mp3"
    await create_call_state(call_uuid, CallStatus.RECORDING.value)
    await handle_recording(call_uuid, recording_url, CallStatus.COMPLETED.value)
    call_state = await get_call_state(call_uuid)
    assert call_state is None
    mock_transcribe_and_translate.assert_called_once_with(call_uuid, recording_url)

@pytest.mark.asyncio
async def test_handle_call_event_service():
    call_uuid = "test-uuid"
    await create_call_state(call_uuid, CallStatus.RECORDING.value)
    await handle_call_event_service(call_uuid, CallStatus.COMPLETED.value)
    call_state = await get_call_state(call_uuid)
    assert call_state is None

@pytest.mark.asyncio
async def test_get_dashboard_data():
    await create_call_state("uuid1", CallStatus.COMPLETED.value)
    await create_call_state("uuid2", CallStatus.COMPLETED.value)
    await create_call_state("uuid3", CallStatus.FAILED.value)
    dashboard_data = await get_dashboard_data()
    assert isinstance(dashboard_data, DashboardData)
    assert dashboard_data.total_recordings == 3
    assert dashboard_data.total_duration == 0
    assert dashboard_data.success_rate == 66.66666666666666
    assert dashboard_data.average_duration == 0

@pytest.mark.asyncio
async def test_get_recordings_data():
    await create_call_state("uuid1", CallStatus.COMPLETED.value)
    await create_call_state("uuid2", CallStatus.COMPLETED.value)
    await create_call_state("uuid3", CallStatus.FAILED.value)
    recordings_data = await get_recordings_data("", 1, 10)
    assert isinstance(recordings_data, dict)
    assert "recordings" in recordings_data
    assert "total" in recordings_data
    assert "page" in recordings_data
    assert "limit" in recordings_data
    assert len(recordings_data["recordings"]) == 3

@pytest.mark.asyncio
@patch("app.crud.create_recording_file", new_callable=AsyncMock)
async def test_create_new_recording(mock_create_recording_file):
    audio = AsyncMock()
    caller_id = "test-caller"
    duration = 60
    mock_create_recording_file.return_value = "test-uuid"
    recording_id = await create_new_recording(audio, caller_id, duration)
    assert recording_id == "test-uuid"
    mock_create_recording_file.assert_called_once_with(audio, caller_id, duration)
