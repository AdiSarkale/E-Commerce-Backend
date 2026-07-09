import pytest

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_readiness(client):
    response = await client.get("/health/ready")

    assert response.status_code == 200
    if response.json()['status'] == 'ready':
        assert response.json()["status"] == 'ready'

    if response.json()['status'] == 'not ready':
        assert response.json()["status"] == 'not ready'
@pytest.mark.asyncio
async def test_liveliness(client):
    response = await client.get('/health/live')
    assert response.status_code == 200
    assert response.json()['status'] == 'live'
