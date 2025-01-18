# services.py
import statistics

from app.crud import (
    create_call_state,
    get_call_state,
    delete_call_state,
    get_all_call_states,
    search_call_states,
    create_recording_file,
)
from app.enums import CallStatus
from app.schemas import DashboardData, Recording
from app.vonage_setup import transcribe_and_translate


async def store_call_state(call_uuid: str):
    existing_call_state = await get_call_state(call_uuid)
    if not existing_call_state:
        await create_call_state(call_uuid, CallStatus.RECORDING.value)


async def handle_recording(call_uuid: str, recording_url: str, status: str):
    call_state = await get_call_state(call_uuid)
    if call_state and status == CallStatus.COMPLETED.value:
        await transcribe_and_translate(call_uuid, recording_url)
        await delete_call_state(call_uuid)


async def handle_call_event_service(call_uuid: str, status: str):
    call_state = await get_call_state(call_uuid)
    if call_state and status == CallStatus.COMPLETED.value:
        await delete_call_state(call_uuid)


async def get_dashboard_data():
    call_states = await get_all_call_states()

    total_recordings = len(call_states)
    total_duration = sum(call.duration for call in call_states if call.duration)
    successful_calls = sum(
        1 for call in call_states if call.status == CallStatus.COMPLETED.value
    )

    success_rate = (
        (successful_calls / total_recordings) * 100 if total_recordings > 0 else 0
    )
    average_duration = (
        statistics.mean(call.duration for call in call_states if call.duration)
        if total_recordings > 0 and any(call.duration for call in call_states)
        else 0
    )

    return DashboardData(
        total_duration=total_duration,
        total_recordings=total_recordings,
        success_rate=success_rate,
        average_duration=average_duration,
    )


async def get_recordings_data(search: str, page: int, limit: int):
    paginated_call_states, total = await search_call_states(search, page, limit)
    recordings = [
        Recording(
            id=call.id,
            date=call.created_at.isoformat(),
            duration=call.duration,
            caller_id=call.caller_id,
            status=call.status,
            user_id=call.user_id,
            user_role=call.user_role,
        )
        for call in paginated_call_states
    ]
    return {
        "recordings": recordings,
        "total": total,
        "page": page,
        "limit": limit,
    }


async def create_new_recording(audio, caller_id: str, duration: int):
    return await create_recording_file(audio, caller_id, duration)
