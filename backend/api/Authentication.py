from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db

from schema.auth import AuthResponse, AuthRequest, RefreshRequest, LogOutResposne
from services.auth import AuthService
from utils.auth import oauth2_scheme


from schema.auth import AuthRequest

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post("/token")
async def login(
    payload: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await AuthService.login(
            db,
            payload.username,  # <-- email goes here
            payload.password
        )
    except Exception as e:
        return {"error":str(e)}


@router.post("/login")
async def login(
    payload: AuthRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService.login(
        db,
        payload.email,
        payload.password
    )

@router.post('/refresh')
async def refresh(
    payload: RefreshRequest
    ):

    return await (AuthService.refresh_token(payload.refresh_token))

@router.post('/logout', response_model=LogOutResposne)
async def logout(
    token: str = Depends(oauth2_scheme)):

    return await AuthService.logout(token)
