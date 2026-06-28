from jose import jwt, JWTError
from datetime import datetime, timedelta

from core.config import settings



def create_access_token(
    user_id: int):

    expire = (
        datetime.utcnow() + timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    payload = {
        "sub" : str(user_id),
        "exp" : expire
        }

    return jwt.encode(
        payload,77,
        settings.SECRET_KEY,
        algorithm= settings.ALGORITHM)


def create_refresh_token(
    user_id: int):
    payload = {
        "sub" : str(user_id),
        "type": "refresh",
        "exp" : datetime.utcnow() + timedelta(days=7)
        }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)

def decode_token(
    token: str):
    try:
        payload = jwt.decode(
            token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        return payload
    except JWTError:
        return None


