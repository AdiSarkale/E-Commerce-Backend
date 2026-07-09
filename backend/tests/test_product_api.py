import pytest
import pytest_asyncio
from random import randint
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_get_all(client):
    response = await client.get(
        '/products/')
    assert response.status_code == 200

@pytest_asyncio.fixture
async def create_product(client):
    response = await client.post(
        '/products/',
        json={
            "name" : fake.color_name(),
            "description" : fake.paragraph(),
            "price" : randint(10,100000) // 10
            })
    return response.json()['data']['id']


@pytest.fixture
async def get_by_id(client,create_product):
    response = await client.get(
        '/products/{prod_id}',
        json = {"prod_id" : create_product})

    assert response.status_code == 200
    return response.json()

@pytest_asyncio.fixture
async def test_update_prod(client,create_product,get_by_id):
    response = await client.put(
        '/products/{prod_id}',
        json = {
            'prod_id' : create_product,
            'name' : get_by_id['name'],
            'description' : get_by_id['description'],
            'price' : get_by_id['price'] + (get_by_id['price'] * 0.25),
            }
        )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete(client,create_product):
    response = await client.delete(
        f'/products/{create_product}')

    assert response.status_code == 200
