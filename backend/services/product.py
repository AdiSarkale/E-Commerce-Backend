from sqlalchemy.ext.asyncio import AsyncSession
from repository.product import ProductRepository
from schema.product import ProductCreate, ProductUpdate, ProductResponse
from fastapi import HTTPException
from utils.cache import CacheManager

class ProductService:


    @staticmethod
    async def products(db: AsyncSession):
        product = await ProductRepository.products(db)
        return product


    @staticmethod
    async def product_by_id(db: AsyncSession , product_id: int):

        cached_key = f'product:{product_id}'

        cached = await CacheManager.get(cached_key)

        if cached:
            return ProductResponse.model_validate_json(cached)

        product = await ProductRepository.get_by_id(db,product_id)

        response = ProductResponse.model_validate(product)

        await CacheManager.set(
            cached_key,
            response.model_dump_json(),
            ttl=300)
        return response

    @staticmethod
    async def create_product(db: AsyncSession, product: ProductCreate):
        created_product = await ProductRepository.create_product(db, product)
        return created_product

    @staticmethod
    async def update_product(db: AsyncSession, prod_id: int, product_update_data: ProductUpdate):
        cached_key = f'product:{prod_id}'
        updated_product = await ProductRepository.update_product(db, prod_id, product_update_data)
        await CacheManager.delete(cached_key)
        return updated_product

    @staticmethod
    async def delete_product(db: AsyncSession, prod_id: int):
        cached_key = f'product:{prod_id}'
        deleted_product_id = await ProductRepository.delete_product(db, prod_id)
        await CacheManager.delete(cached_key)

        if not deleted_product_id:
            raise HTTPException(404, detail='No Such Product Found to Delete')
        return deleted_product_id
