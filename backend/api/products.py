from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schema.product import ProductResponse, ProductCreate, ProductUpdate, ProductDeleteResponse
from schema.api import ApiResponse
from services.product import ProductService
from db import get_db

router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/',response_model=ApiResponse[list[ProductResponse]])
async def products(
    db: AsyncSession = Depends(get_db)
        ):
    prods = await ProductService.products(db)

    return ApiResponse(success=True, message='Products fetched successfully', data=[p for p in prods])




@router.get('/{prod_id}',response_model=ApiResponse[ProductResponse])
async def get_by_id(
    prod_id: int,
    db: AsyncSession = Depends(get_db)
    ):

    prod = await ProductService.product_by_id(db, prod_id)

    if not prod:
        raise HTTPException(404,detail='NO PRODUCTS FOUND')

    return ApiResponse(success=True,message='Products fetched successfully by id', data=ProductResponse.model_validate(prod))


@router.post('/',response_model=ApiResponse[ProductResponse])
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    created_product = await ProductService.create_product(db, product)
    return ApiResponse(success=True, message='Product created successfully', data=ProductResponse.model_validate(created_product))

@router.put('/{prod_id}',response_model=ApiResponse[ProductResponse])
async def update_product(
    prod_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_product = await ProductService.update_product(db, prod_id, product)
    return ApiResponse(success=True, message='Product updated successfully', data=ProductResponse.model_validate(updated_product))

@router.delete('/{prod_id}', response_model=ApiResponse)
async def delete_product(
    prod_id: int,
    db: AsyncSession = Depends(get_db)
    ):

    await ProductService.delete_product(db,prod_id)

    return ApiResponse(success=True,message='Product Deleted Successfully', data=prod_id)
