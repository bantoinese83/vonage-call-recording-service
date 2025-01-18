from fastapi import Request, HTTPException
from vonage import Vonage, Auth
from halo import Halo
from loguru import logger
from sqlalchemy import select, exists

from app.config import VONAGE_API_KEY, VONAGE_API_SECRET, VONAGE_NUMBER
from app.database import async_session
from app.enums import CallStatus
from googletrans import Translator
import speech_recognition as sr
from app.aws_setup import upload_file_to_s3, AWS_BUCKET_NAME
from app.models import CallState
import aiohttp

auth = Auth(api_key=VONAGE_API_KEY, api_secret=VONAGE_API_SECRET)
vonage_client = Vonage(auth=auth)
voice = vonage_client.voice

def create_ncco(request: Request):
    return [
        {
            "action": "talk",
            "text": "This call will be recorded for quality assurance purposes.",
        },
        {
            "action": "record",
            "eventUrl": [f"{request.base_url}api/v1/calls/recordings"],
            "beepStart": False,
        },
        {
            "action": "connect",
            "endpoint": [
                {
                    "type": "phone",
                    "number": VONAGE_NUMBER,
                }
            ],
        },
    ]

async def store_call_state(call_uuid: str):
    spinner = Halo(text="Storing call state", spinner="dots")
    spinner.start()
    async with async_session() as session:
        async with session.begin():
            existing_call_state = await session.execute(
                select(exists().where(CallState.uuid == call_uuid))
            )
            existing_call_state = existing_call_state.scalar_one_or_none()
            if not existing_call_state:
                call_state = CallState(
                    uuid=call_uuid, status=CallStatus.RECORDING.value
                )
                session.add(call_state)
            else:
                logger.info(f"Call state with uuid {call_uuid} already exists")
    spinner.succeed("Call state stored successfully")

async def handle_recording(call_uuid: str, recording_url: str, status: str):
    spinner = Halo(text="Handling recording event", spinner="dots")
    spinner.start()
    async with async_session() as session:
        async with session.begin():
            call_state = await session.get(CallState, call_uuid)
            if call_state:
                if status == CallStatus.RECORDING.value:
                    logger.info(f"Recording started for call {call_uuid}")
                elif status == CallStatus.COMPLETED.value:
                    logger.info(
                        f"Recording completed for call {call_uuid}. URL: {recording_url}"
                    )
                    await transcribe_and_translate(call_uuid, recording_url)
                    await session.delete(call_state)
                elif status == CallStatus.FAILED.value:
                    logger.error(f"Recording failed for call {call_uuid}")
                    await session.delete(call_state)
    spinner.succeed("Recording event handled successfully")

async def handle_call_event(call_uuid: str, status: str):
    spinner = Halo(text="Handling call event", spinner="dots")
    spinner.start()
    async with async_session() as session:
        async with session.begin():
            call_state = await session.get(CallState, call_uuid)
            if call_state and status == CallStatus.COMPLETED.value:
                logger.info(f"Call {call_uuid} completed")
                await session.delete(call_state)
    spinner.succeed("Call event handled successfully")

async def transcribe_and_translate(call_uuid: str, recording_url: str):
    recognizer = sr.Recognizer()
    translator = Translator()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(recording_url) as response:
                if response.status == 200:
                    with open(f"{call_uuid}.wav", "wb") as f:
                        f.write(await response.read())
                else:
                    raise HTTPException(status_code=500, detail="Failed to download recording")

        with sr.AudioFile(f"{call_uuid}.wav") as source:
            audio = recognizer.record(source)
        transcript = recognizer.recognize_sphinx(audio)
        translation = await translator.translate(transcript, dest="es")
        translation_text = translation.text

        async with async_session() as session:
            async with session.begin():
                call_state = await session.get(CallState, call_uuid)
                if call_state:
                    call_state.transcript = transcript
                    call_state.translation = translation_text
                    session.add(call_state)

        s3_url = upload_file_to_s3(f"{call_uuid}.wav", AWS_BUCKET_NAME, f"{call_uuid}.wav")
        logger.info(f"Audio file uploaded to S3: {s3_url}")
        logger.info(f"Transcript: {transcript}")
        logger.info(f"Translation: {translation_text}")
    except Exception as e:
        logger.error(f"Error during transcription or translation: {e}")
        raise HTTPException(status_code=500, detail="Failed to process recording")
