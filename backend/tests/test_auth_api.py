import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def login(client):
    response = await client.post(
        '/auth/login',
        json={
            'email' : 'adisarkale@gmail.com',
            'password' : '123456'
            })

    assert response.status_code == 200
    return response.json()['access_token']

@pytest_asyncio.fixture
async def auth_headers(client,login):
    return {
        'Authorization' : f'Bearer {login}'
        }
@pytest.mark.asyncio
async def test_logout(client,auth_headers):
    response = await client.post(
        '/auth/logout',
        headers=auth_headers
        )
    assert response.status_code == 200
