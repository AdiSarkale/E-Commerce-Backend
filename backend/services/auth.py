from utils.password_hasher import PasswordHasher
from utils.josewt import create_access_token, create_refresh_token, decode_token
from repository.auth import AuthRepository
from utils.cache import CacheManager
from datetime import time



class AuthService:

    @staticmethod
    async def login(
        db,
        email: str,
        password: str):



        user = await AuthRepository.get_by_email(db,email)

        if not user:
            raise ValueError(f" No User available with Email: {email}")

        if not PasswordHasher.verify_hash(password=password,hashed_password=user.hashed_password):

            raise ValueError('Invalid Credentials')

        token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)



        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "token_type" : "bearer"}

    @staticmethod
    async def refresh_token(
            refresh_token: str):

        payload = decode_token(refresh_token)

        if payload['type'] != 'refresh':

            raise ValueError("Invalid Refresh Token")
        user_id = int(payload['sub'])

        new_access_token = (create_access_token(user_id))

        return {
            "access_token" : new_access_token
            }

    @staticmethod
    async def logout(
        token: str):
        payload = decode_token(token)

        if not payload:
            raise ValueError('Invalid Token')

        exp = payload.get('exp')
        if not exp:
            raise ValueError('Invalid TOken')

        ttl = exp - int(time.time())

        if ttl > 0:
            await CacheManager.set(f"jwt:blacklist:{token}","1",ex=ttl)

        return {
            'message' : "Logout Successful"
            }
