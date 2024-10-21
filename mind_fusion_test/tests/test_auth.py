import os
import pytest


@pytest.mark.asyncio
async def test_register(ac):

    request_data = {
            "email": "test1@test.com",
            "password": "testpassword123",
            "tg_id": 100500100
        }
    response = await ac.post("/api/auth/register",  json=request_data)
    assert response.status_code == 201


