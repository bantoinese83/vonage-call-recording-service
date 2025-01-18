import os
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.config import LOG_FILE
from app.database import init_db
from app.routes import router

logger.add(LOG_FILE, rotation="1 day")

@asynccontextmanager
async def lifespan(app_context: FastAPI):
    await init_db()
    yield

# FastAPI app configuration
app = FastAPI(
    title="Vonage Call Recording",
    description="A simple call recording service using Vonage Voice API",
    version="0.1.0",
    lifespan=lifespan,
)

# Include the routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)