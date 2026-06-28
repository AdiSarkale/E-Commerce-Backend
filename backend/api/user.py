from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schema.user import UserCreate, UserResponse, UserUpdate
from schema.api import ApiResponse
from services.cart import CartService
from services.user import UserService
from db import get_db
from utils.auth import get_current_user
import re


router = APIRouter(prefix='/users',tags=['Users'])


@router.get('/',response_model=ApiResponse[list[UserResponse]])
async def users_all(
    db: AsyncSession = Depends(get_db)
    ):

    users = await UserService.get_all(db)
    if users:
        return ApiResponse(success=True, message='Users Fetched Sucessfully', data=[UserResponse.model_validate(user) for user in users])

    return ApiResponse(success=False, message='No Users in the Database', data=[])


@router.post('/',response_model=ApiResponse[UserResponse])
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
    ):

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.search(email_pattern, user.email):
        return ApiResponse(success=False, message='Invalid Email ID Entered', data=None)
    new_user = await UserService.create(user,db)
    print('USER: ',UserResponse.model_validate(new_user))
    if not new_user:
        return ApiResponse(success=False, message='User with this email already exists', data=None)
    return ApiResponse(success=True, message='User Created Sucessfully', data=UserResponse.model_validate(new_user))


@router.get('/me',response_model=ApiResponse[UserResponse])
async def get_me(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    user = await UserService.get_by_id(current_user.id, db)
    if not user:
        return ApiResponse(success=False, message='User not found', data=None)
    return ApiResponse(success=True, message='User fetched successfully', data=UserResponse.model_validate(user))


@router.delete('/me',response_model=ApiResponse[UserResponse])
async def delete_user(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    deleted = await UserService.delete(current_user.id,db)

    if not deleted:
        return ApiResponse(success=False, message='User not Found', data=None)
    return ApiResponse(success=True,message='User Deleted Successfully', data=None)


@router.put('/me',response_model = ApiResponse[UserResponse])
async def update_user(
    user_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    updated = await UserService.update_user(current_user.id,user_data,db)

    if not updated:
        return ApiResponse(success=False, message='User not Found', data=None)
    return ApiResponse(success=True, message='User Updated Successfully', data=UserResponse.model_validate(updated))
