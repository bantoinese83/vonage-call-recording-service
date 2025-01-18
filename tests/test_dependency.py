import pytest
from fastapi.testclient import TestClient
from main import app
from app.auth import create_access_token
from app.models import User
from app.database import async_session

client = TestClient(app)

@pytest.fixture
async def test_user():
    async with async_session() as session:
        user = User(username="testuser", hashed_password="testpassword")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

@pytest.fixture
def token(test_user):
    access_token = create_access_token(data={"sub": test_user.username})
    return access_token

def test_get_recordings(token):
    response = client.get(
        "/api/v1/recordings",
        headers={"Authorization": f"Bearer {token}"},
        params={"search": "test", "page": 1, "limit": 10},
    )
    assert response.status_code == 200
    data = response.json()
    assert "recordings" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
