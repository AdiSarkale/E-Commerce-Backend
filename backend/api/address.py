from services.address import AddressServices
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schema.api import ApiResponse
from schema.address import AddressResponse, AddressCreate, AddressUpdate
from utils.auth import get_current_user
from db import get_db
import traceback

router = APIRouter(prefix='/address', tags=['Addr'])

@router.post('',response_model=ApiResponse[AddressResponse])
async def add_address(
    addr: AddressCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        result = await AddressServices.create_address(db,addr,current_user.id)

        return ApiResponse(success=True,message='Address Added',data=result)
    except Exception as e:
        return ApiResponse(success=False,message=f'{str(e)}',data=None)


@router.get('',response_model=ApiResponse[list[AddressResponse]])
async def get_user_address(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        result = await AddressServices.get_addr(db,current_user.id)

        return ApiResponse(success=True,message='Fetched Addresses Successfully',data=result)
    except Exception as e:
        return ApiResponse(success=False,message=f'{str(e)}',data=None)

@router.get('/{addr_id}',response_model=ApiResponse[AddressResponse])
async def get_address_by_id(
    addr_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        result = await AddressServices.get_by_id(db,current_user.id,addr_id)
        print(result)
        return ApiResponse(success=True,message='Fetched Addresses Successfully',data=result)
    except Exception as e:
        return ApiResponse(success=False,message=f'{str(e)}',data=None)

@router.put('',response_model=ApiResponse[AddressResponse])
async def update_address(
    addr_id: int,
    addr: AddressUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        result = await AddressServices.update_addr(db,current_user.id,addr,addr_id)

        return ApiResponse(success=True,message='Updated Address Successfully',data=result)
    except Exception as e:
        # return ApiResponse(success=False,message=f'{str(e)}',data=None)
        traceback.print_exc()
        raise HTTPException(404,detail=f'str{e}')


@router.delete('/{addr_id}',response_model=ApiResponse[AddressResponse])
async def delete_address(
    addr_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    try:
        result = await AddressServices.delete_addr(db,current_user.id,addr_id)

        return ApiResponse(success=True,message=f'Address Deleted with ID {addr_id}',data=result)
    except Exception as e:
        return ApiResponse(success=False,message=f'{str(e)}',data=None)


@router.patch('/{addr_id}/default',response_model=ApiResponse[AddressResponse])
async def set_default_addr(
        addr_id: int,
        isDefault: bool,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

    try:
        result = await AddressServices.set_default(
            addr_id=addr_id,
            isDefault=isDefault,
            user_id=current_user.id,
            db=db)


        return ApiResponse(success=True,message='Default Address Changed Successfully',data=result)
    except Exception as e:
        return ApiResponse(success=False,message=f'{str(e)}',data=None)

