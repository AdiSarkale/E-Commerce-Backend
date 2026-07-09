import pytest
import pytest_asyncio
import json
from faker import Faker

fake = Faker()


@pytest_asyncio.fixture
async def create_user(client):
    password = '123456789'
    email = fake.email()
    username = fake.user_name()
    response = await client.post(
        '/users/',
        json={
            'name' : username,
            'email' : email,
            'hashed_password' : password
            })
    assert response.status_code == 200
    # with open('output.txt', 'w') as rw:
    #     rw.write(json.dumps(response.json()))
    print(response.json())
    user = response.json()
    user['data']['hashed_password'] = password

    return user


@pytest_asyncio.fixture
async def login(client,create_user):
    response = await client.post(
        '/auth/login',
        json={
            'email':create_user['data']['email'],
            'password' : create_user['data']['hashed_password']
            }
        )
    assert response.status_code == 200
    # with open('login_output.txt', 'w') as rw:
    #     rw.write(json.dumps(response.json()))
    print(response.json())
    return response.json()['access_token']

@pytest_asyncio.fixture
async def auth_headers(login):
    return {
        "Authorization" : f'Bearer {login}'
        }

@pytest.mark.asyncio
async def test_update_user(client,auth_headers,create_user):
    name = create_user['data']['name']
    email = fake.email()
    response = await client.put(
        '/users/me',
        headers = auth_headers,
        json={
            'name' : name,
            'email' : email,
            })
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_current_user(client,auth_headers):
    response = await client.get(
        '/users/me',
        headers=auth_headers)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_me(client,auth_headers):
    response = await client.delete(
        '/users/me',
        headers=auth_headers,
        )
    assert response.status_code == 200



@pytest.mark.asyncio
async def test_get_all(client):
    response = await client.get(
        '/users/'
        )
    assert response.status_code == 200
