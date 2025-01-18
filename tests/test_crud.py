import pytest
from sqlalchemy import select, delete
from app.database import async_session
from app.models import CallState
from app.crud import (
    create_call_state,
    get_call_state,
    delete_call_state,
    get_all_call_states,
    search_call_states,
    create_recording_file,
)
from app.enums import CallStatus

@pytest.fixture(autouse=True)
async def clear_database():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(CallState))
            await session.commit()

@pytest.mark.asyncio
async def test_create_call_state():
    await create_call_state("test-uuid", CallStatus.RECORDING.value)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == "test-uuid"))
            call_state = result.scalar_one_or_none()
            assert call_state is not None
            assert call_state.status == CallStatus.RECORDING.value

@pytest.mark.asyncio
async def test_get_call_state():
    await create_call_state("test-uuid", CallStatus.RECORDING.value)
    call_state = await get_call_state("test-uuid")
    assert call_state is not None
    assert call_state.status == CallStatus.RECORDING.value

@pytest.mark.asyncio
async def test_delete_call_state():
    await create_call_state("test-uuid", CallStatus.RECORDING.value)
    await delete_call_state("test-uuid")
    call_state = await get_call_state("test-uuid")
    assert call_state is None

@pytest.mark.asyncio
async def test_get_all_call_states():
    await create_call_state("test-uuid-1", CallStatus.RECORDING.value)
    await create_call_state("test-uuid-2", CallStatus.RECORDING.value)
    call_states = await get_all_call_states()
    assert len(call_states) == 2

@pytest.mark.asyncio
async def test_search_call_states():
    await create_call_state("test-uuid-1", CallStatus.RECORDING.value)
    await create_call_state("test-uuid-2", CallStatus.RECORDING.value)
    call_states, total = await search_call_states("test", 1, 10)
    assert len(call_states) == 2
    assert total == 2

@pytest.mark.asyncio
async def test_create_recording_file():
    audio_content = b"test audio content"
    audio_file = type("File", (object,), {"file": type("File", (object,), {"read": lambda: audio_content})})()
    recording_id = await create_recording_file(audio_file, "test-caller", 60)
    assert recording_id is not None
