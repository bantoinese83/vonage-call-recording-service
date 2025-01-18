# decorators.py
from functools import wraps
from fastapi import HTTPException
from loguru import logger

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            logger.error(f"HTTPException: {e.detail}")
            raise
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    return wrapper