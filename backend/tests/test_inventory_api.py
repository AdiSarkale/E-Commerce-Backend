import pytest
import pytest_asyncio
from random import randint

@pytest_asyncio.fixture
async def get_count(client):
    response = await client.get(
        'products/'
        )

    assert response.status_code == 200
    count = len(response.json()['data'])
    id = randint(1,count)
    return id

@pytest_asyncio.fixture
async def get_inv_info(client,get_count):
    response = await client.get(
        f"/inventory/{get_count}")
    response.status_code == 200
    return response.json()['data']

@pytest_asyncio.fixture
async def create_inv(client,get_inv_info):
    quantity = get_inv_info['quantity']
    response = await client.post(
        '/inventory/',
        json = {
            'product_id' : get_count,
            'quantity' :  quantity
            }
        )
    assert response.status_code == 200
    return response.json()['data']

@pytest.mark.asyncio
async def update_inv(client,get_inv_info):
    q = get_inv_info['quantity']
    response = await client.put(
        f'/inventory/{get_inv_info["product_id"]}',
        json = {
            'quantity' : q + (q * 0.25)
                }
    )
    assert response.status_code == 200




