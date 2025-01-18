import pytest
from unittest.mock import patch, AsyncMock

from app.models import CallState
from app.vonage_setup import create_ncco, store_call_state, handle_recording, handle_call_event, transcribe_and_translate
from fastapi import Request
from app.enums import CallStatus
from app.database import async_session
from sqlalchemy import select, delete

@pytest.fixture(autouse=True)
async def clear_database():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(CallState))
            await session.commit()

@pytest.mark.asyncio
async def test_create_ncco():
    request = Request(scope={"type": "http", "base_url": "http://testserver", "headers": []})
    ncco = create_ncco(request)
    assert isinstance(ncco, list)
    assert len(ncco) == 3
    assert ncco[0]["action"] == "talk"
    assert ncco[1]["action"] == "record"
    assert ncco[2]["action"] == "connect"

@pytest.mark.asyncio
async def test_store_call_state():
    call_uuid = "test-uuid"
    await store_call_state(call_uuid)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == call_uuid))
            call_state = result.scalar_one_or_none()
            assert call_state is not None
            assert call_state.uuid == call_uuid
            assert call_state.status == CallStatus.RECORDING.value

@pytest.mark.asyncio
@patch("app.vonage_setup.transcribe_and_translate", new_callable=AsyncMock)
async def test_handle_recording(mock_transcribe_and_translate):
    call_uuid = "test-uuid"
    recording_url = "http://testserver/recording.mp3"
    await store_call_state(call_uuid)
    await handle_recording(call_uuid, recording_url, CallStatus.COMPLETED.value)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == call_uuid))
            call_state = result.scalar_one_or_none()
            assert call_state is None
    mock_transcribe_and_translate.assert_called_once_with(call_uuid, recording_url)

@pytest.mark.asyncio
async def test_handle_call_event():
    call_uuid = "test-uuid"
    await store_call_state(call_uuid)
    await handle_call_event(call_uuid, CallStatus.COMPLETED.value)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == call_uuid))
            call_state = result.scalar_one_or_none()
            assert call_state is None

@pytest.mark.asyncio
@patch("app.vonage_setup.upload_file_to_s3", return_value="http://mock_s3_url/recording.mp3")
@patch("app.vonage_setup.Translator.translate", return_value=AsyncMock(text="translated text"))
@patch("app.vonage_setup.sr.Recognizer.recognize_sphinx", return_value="transcribed text")
@patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
async def test_transcribe_and_translate(mock_get, mock_recognize_sphinx, mock_translate, mock_upload_file_to_s3):
    mock_get.return_value.__aenter__.return_value.read.return_value = b"audio data"
    call_uuid = "test-uuid"
    recording_url = "http://testserver/recording.mp3"
    await store_call_state(call_uuid)
    await transcribe_and_translate(call_uuid, recording_url)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == call_uuid))
            call_state = result.scalar_one_or_none()
            assert call_state is not None
            assert call_state.transcript == "transcribed text"
            assert call_state.translation == "translated text"
