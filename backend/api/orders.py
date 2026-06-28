from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.order import OrderService
from schema.order import CheckoutResponse, OrderResponse
from schema.api import ApiResponse
from db import get_db
from utils.auth import get_current_user


router = APIRouter(prefix='/order',tags=['Order'])


@router.post("/checkout",response_model=CheckoutResponse)
async def checkout(
    current_user = Depends(get_current_user),
    db: AsyncSession= Depends(get_db),
    ):

    try:
        return await OrderService.checkout(db,current_user.id)

    except ValueError as e:
        raise HTTPException(400,detail=str(e))

@router.get('',response_model=ApiResponse[list[OrderResponse]])
async def getOrders(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    result = await OrderService.get_orders(db,current_user.id)
    print(result)
    return ApiResponse(success=True, message='Orders Fetched', data=result)


