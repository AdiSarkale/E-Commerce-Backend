from fastapi import APIRouter, Depends, HTTPException

from services.inventory import InventoryService
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schema.api import ApiResponse
from repository.inventory import InventoryRepository
from schema.inventory import InventoryResponse, InventoryCreate, InventoryUpdate


router = APIRouter(prefix='/inventory',tags=['Inventory'])

@router.post("",response_model=ApiResponse[InventoryResponse])
async def create_inventory(
    payload:  InventoryCreate,
    db: AsyncSession = Depends(get_db)):

    existing = await InventoryRepository.get_by_product(db,payload.product_id)

    if existing:
        return ApiResponse(success=False, message='Inventory Already Exists', data=InventoryResponse.model_validate(existing) )


    res = await InventoryService.create_inventory(db,payload.product_id, payload.quantity)

    return ApiResponse(sucess=True, message='Inventory Created Succesfully', data=InventoryResponse.model_validate(res) )


@router.get('/product/{product_id}',response_model=ApiResponse[InventoryResponse])
async def get_inventory(
    product_id: int,
    db: AsyncSession = Depends(get_db)):
    try:
        res = await InventoryService.get_by_id(db,product_id)
        return ApiResponse(success=True, message='Inventory Fetched Successfully', data=res)
    except Exception as e:
        return ApiResponse(success=True, message=f'{str(e)}', data=None)


@router.post(
    "/product/{product_id}",
    response_model=ApiResponse[InventoryResponse]
)
async def update_inv(
    product_id: int,
    inv: InventoryUpdate,
    db: AsyncSession = Depends(get_db)
):

    inventory = await InventoryRepository.get_by_product(
        db,
        product_id
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    inventory = await InventoryRepository.increase_stock(
        db,
        inventory,
        inv.quantity
    )

    return ApiResponse(
        success=True,
        message=f"Increased stock by {inv.quantity}",
        data=InventoryResponse.model_validate(inventory)
    )
