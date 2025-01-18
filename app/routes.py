from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request, Query, UploadFile, Form, File
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    Token,
    User,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_user,
)
from app.decorators import handle_exceptions
from app.schemas import CallEvent, DashboardData, Recording, RecordingEvent, UserCreate
from app.services import (
    store_call_state,
    get_dashboard_data,
    get_recordings_data,
    create_new_recording,
    handle_call_event_service,
    handle_recording,
)
from app.vonage_setup import create_ncco

router = APIRouter()


@router.post(
    "/auth/signup",
    response_model=User,
    tags=["Authentication"],
    summary="Sign up new user",
    description="Register a new user by providing username, password, and optional details.",
)
async def sign_up(user: UserCreate):
    new_user = await create_user(user)
    return new_user


@router.post(
    "/auth/login",
    response_model=Token,
    tags=["Authentication"],
    summary="Login for access token",
    description="Authenticate user and return a JWT token.",
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/auth/user",
    response_model=User,
    tags=["Authentication"],
    summary="Get current user",
    description="Retrieve the currently authenticated user's information.",
)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post(
    "/calls/answer",
    response_class=JSONResponse,
    tags=["Calls"],
    summary="Answer call",
    description="Answer an incoming call and return NCCO actions.",
)
@handle_exceptions
async def answer_call(request: Request, uuid: str = Query(..., min_length=1)):
    ncco = create_ncco(request)
    await store_call_state(uuid)
    return JSONResponse(ncco)


@router.post(
    "/calls/events",
    response_class=JSONResponse,
    tags=["Calls"],
    summary="Handle call event",
    description="Handle a call event and update the call state.",
)
@handle_exceptions
async def handle_call_event(event: CallEvent):
    await handle_call_event_service(event.uuid, event.status)
    return JSONResponse({"status": "ok"})


@router.post(
    "/calls/recordings",
    response_class=JSONResponse,
    tags=["Calls"],
    summary="Handle recording event",
    description="Handle a recording event and update the call state.",
)
@handle_exceptions
async def handle_recording_event(event: RecordingEvent):
    await handle_recording(event.uuid, event.url, event.status)
    return JSONResponse({"status": "ok"})


@router.get(
    "/recordings/list",
    response_model=List[Recording],
    tags=["Recordings"],
    summary="Get recordings",
    description="Retrieve a list of recordings with optional search, pagination, and limit parameters.",
)
@handle_exceptions
async def list_recordings(
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


@router.get(
    "/dashboard/data",
    response_model=DashboardData,
    tags=["Dashboard"],
    summary="Get dashboard data",
    description="Retrieve dashboard data including total duration, total recordings, success rate, and average duration.",
)
@handle_exceptions
async def get_dashboard_data_route():
    return await get_dashboard_data()


@router.post(
    "/recordings/create",
    response_class=JSONResponse,
    tags=["Recordings"],
    summary="Create recording",
    description="Create a new recording by uploading an audio file and providing caller ID and duration.",
)
@handle_exceptions
async def create_recording(
    audio: UploadFile = File(...), caller_id: str = Form(...), duration: int = Form(...)
):
    recording_id = await create_new_recording(audio, caller_id, duration)
    return JSONResponse(
        {
            "status": "success",
            "recording_id": recording_id,
        }
    )
