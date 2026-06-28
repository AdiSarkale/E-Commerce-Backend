from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError
from utils.josewt import decode_token
from db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils.cache import CacheManager
from repository.user import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user(db: AsyncSession = Depends(get_db),token:str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    print("TOKEN:", token)
    print("PAYLOAD:", payload)

    if not payload:
        raise HTTPException(
            status_code=401,detail='Invalid Token')

    blacklisted = await CacheManager.get(f'jwt:blaclist:{token}')
    if blacklisted:
        raise HTTPException(
            401,
            detial='Token Revoked')
    user_id = int(payload["sub"])

    user = await UserRepository.get_by_id(db=db, id=user_id)

    if not user:
        raise HTTPException(
            status=401, detail='User Not Found')

    return user
