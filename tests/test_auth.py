import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from unittest.mock import patch, MagicMock

from app.auth import (
    create_user,
    verify_password,
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    Token,
    TokenData,
)
from app.database import async_session
from app.models import User as UserModel
from app.schemas import UserCreate

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


@pytest.mark.asyncio
async def test_create_user():
    user_create = UserCreate(username="testuser", password="testpassword")
    user = create_user(user_create)
    assert user.username == "testuser"
    assert verify_password("testpassword", user.hashed_password)


def test_verify_password():
    hashed_password = pwd_context.hash("testpassword")
    assert verify_password("testpassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_get_password_hash():
    hashed_password = get_password_hash("testpassword")
    assert pwd_context.verify("testpassword", hashed_password)


@pytest.mark.asyncio
async def test_get_user():
    async with async_session() as session:
        async with session.begin():
            user = UserModel(username="testuser", hashed_password="testpassword")
            session.add(user)
            await session.commit()

        user = await get_user("testuser")
        assert user.username == "testuser"


@pytest.mark.asyncio
async def test_authenticate_user():
    async with async_session() as session:
        async with session.begin():
            user = UserModel(username="testuser", hashed_password=get_password_hash("testpassword"))
            session.add(user)
            await session.commit()

        user = await authenticate_user("testuser", "testpassword")
        assert user.username == "testuser"

        user = await authenticate_user("testuser", "wrongpassword")
        assert not user


def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"


@pytest.mark.asyncio
async def test_get_current_user():
    async with async_session() as session:
        async with session.begin():
            user = UserModel(username="testuser", hashed_password="testpassword")
            session.add(user)
            await session.commit()

        token = create_access_token({"sub": "testuser"})
        current_user = await get_current_user(token)
        assert current_user.username == "testuser"


@pytest.mark.asyncio
async def test_get_current_active_user():
    async with async_session() as session:
        async with session.begin():
            user = UserModel(username="testuser", hashed_password="testpassword", disabled=False)
            session.add(user)
            await session.commit()

        token = create_access_token({"sub": "testuser"})
        current_user = await get_current_active_user(token)
        assert current_user.username == "testuser"

        user.disabled = True
        await session.commit()

        with pytest.raises(HTTPException):
            await get_current_active_user(token)


def test_token_model():
    token = Token(access_token="testtoken", token_type="bearer")
    assert token.access_token == "testtoken"
    assert token.token_type == "bearer"


def test_token_data_model():
    token_data = TokenData(username="testuser")
    assert token_data.username == "testuser"
