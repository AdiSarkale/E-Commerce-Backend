import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_get_all(client):
    response = await client.get(
        '/products/')

