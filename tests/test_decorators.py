import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock

from app.decorators import handle_exceptions

@pytest.mark.asyncio
async def test_handle_exceptions_decorator_success():
    @handle_exceptions
    async def sample_function():
        return "Success"

    result = await sample_function()
    assert result == "Success"

@pytest.mark.asyncio
async def test_handle_exceptions_decorator_http_exception():
    @handle_exceptions
    async def sample_function():
        raise HTTPException(status_code=400, detail="Bad Request")

    with pytest.raises(HTTPException) as exc_info:
        await sample_function()
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Bad Request"

@pytest.mark.asyncio
async def test_handle_exceptions_decorator_general_exception():
    @handle_exceptions
    async def sample_function():
        raise Exception("General Error")

    with pytest.raises(HTTPException) as exc_info:
        await sample_function()
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal Server Error"
