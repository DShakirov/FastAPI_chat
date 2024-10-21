from httpx import AsyncClient

import pytest


from main import app



@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac






