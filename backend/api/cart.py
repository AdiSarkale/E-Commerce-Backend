from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schema.api import ApiResponse
from schema.cart import CartItemResponse, CartResponse, CartAddItem
from services.cart import CartService
from utils.auth import get_current_user


router = APIRouter(prefix='/cart', tags=['Cart'])


@router.post('/add', response_model=ApiResponse[CartItemResponse], status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
    cart_item: CartAddItem,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        cart =  await CartService.add_to_cart(
            db=db,
            user_id = current_user.id,
            product_id=cart_item.product_id,
            quantity = cart_item.quantity)
        return ApiResponse(success=True, message=f'Cart successfully created ', data=CartItemResponse.model_validate(cart))
    except ValueError as e:
        return ApiResponse(success=False, message=f"{str(e)}",data=[    ])


@router.get('/',response_model=ApiResponse[CartResponse])
async def get_cart(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    cart= await CartService.get_cart(db,current_user.id)
    return ApiResponse(success=True,message=f'Cart Fetched',data=cart)



@router.put('/',response_model=CartItemResponse)
async def update_quantity(
    quantity: int,
    product_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    cart = await CartService.quantity_update(db,current_user.id,quantity,product_id)
    return ApiResponse(success=True,message=f'Cart Item Quantity Updated to {quantity}',data=CartItemResponse.model_validate(cart))


@router.delete('/items/{item_id}',response_model=CartResponse)
async def  delete_item(
    item_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    await CartService.delete_cart_item(db,current_user.id, item_id)
    return ApiResponse(success=True,message=f'Item with ID: {item_id} removed from Cart',data=None)
