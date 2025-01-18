from fastapi import APIRouter, Depends
from app.auth import get_current_active_user, User
from app.schemas import Recording
from app.services import get_recordings_data
from fastapi import Query
from typing import List
from fastapi.responses import JSONResponse
from app.decorators import handle_exceptions


router = APIRouter()


@router.get("/v1/recordings", response_model=List[Recording])
@handle_exceptions
async def get_recordings(
    search: str = Query(None, min_length=1),
    page: int = Query(1),
    limit: int = Query(10),
    current_user: User = Depends(get_current_active_user),
):
    recordings_data = await get_recordings_data(search, page, limit)
    recordings_data["recordings"] = [
        recording.dict() for recording in recordings_data["recordings"]
    ]
    return JSONResponse(recordings_data)
