from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from db import get_db
from core.cache import cached

from fastapi import Depends

router = APIRouter(prefix='/health',tags=['Health'])


@router.get('/')
async def health():
    return {
        "status":'healthy'
        }


@router.get('/ready')
async def readiness(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(cached)
    ):

    db_status = 'connected'
    redis_status = 'connected'

    try:
        await db.execute(text('SELECT 1'))
    except Exception:
        db_status = 'disconnected'

    try:
        await redis.ping()
    except Exception:
        redis_status = 'discontinued'

    healthy = (
        db_status == 'connected' and redis_status == 'connected'
        )

    return{
        "status" : 'ready' if healthy else 'not ready',
        'database_status' : db_status,
        'redis_status' : redis_status
        }

@router.get('/live')
async def live():
    return {
        'status' : 'live'
        }

