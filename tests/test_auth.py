import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from app.main import app
from app.core.config import settings


@pytest.mark.asyncio
async def test_register_and_login():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            res = await ac.post(
                settings.API_V1_PREFIX + "/auth/register",
                json={"email": "u1@example.com", "password": "pass"},
            )
            assert res.status_code == 201, res.text
            res_login = await ac.post(
                settings.API_V1_PREFIX + "/auth/login",
                data={"username": "u1@example.com", "password": "pass"},
            )
            assert res_login.status_code == 200
            data = res_login.json()
            assert "access_token" in data
            assert "refresh_token" in data
