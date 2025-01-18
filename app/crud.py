# crud.py
import os
import uuid

from sqlalchemy import func
from sqlmodel import select, delete

from app.aws_setup import upload_file_to_s3, AWS_BUCKET_NAME
from app.database import async_session
from app.enums import CallStatus
from app.models import CallState


async def create_call_state(call_uuid: str, status: str):
    async with async_session() as session:
        async with session.begin():
            existing_call_state = await session.execute(
                select(CallState).where(CallState.uuid == call_uuid)
            )
            if existing_call_state.scalar_one_or_none() is None:
                call_state = CallState(uuid=call_uuid, status=status)
                session.add(call_state)

async def get_call_state(call_uuid: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState).where(CallState.uuid == call_uuid))
            return result.scalar_one_or_none()

async def delete_call_state(call_uuid: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(CallState).where(CallState.uuid == call_uuid))

async def get_all_call_states():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(CallState))
            return result.scalars().all()

async def search_call_states(search: str, page: int, limit: int):
    async with async_session() as session:
        async with session.begin():
            query = select(CallState)
            if search:
                query = query.where(
                    func.coalesce(CallState.caller_id, "").like(f"%{search}%")
                )
            result = await session.execute(query)
            call_states = result.scalars().all()
            total = len(call_states)
            start = (page - 1) * limit
            end = start + limit
            paginated_call_states = call_states[start:end]
            return paginated_call_states, total

async def create_recording_file(audio, caller_id: str, duration: int):
    filename = f"{uuid.uuid4()}.wav"
    with open(filename, "wb") as buffer:
        buffer.write(audio.file.read())

    s3_url = upload_file_to_s3(filename, AWS_BUCKET_NAME, filename)

    async with async_session() as session:
        async with session.begin():
            new_call = CallState(
                uuid=str(uuid.uuid4()),
                status=CallStatus.COMPLETED.value,
                caller_id=caller_id,
                duration=duration,
                recording_url=s3_url,
            )
            session.add(new_call)

    os.remove(filename)
    return new_call.uuid
