from sqlalchemy import select
from models.user import User


class AuthRepository:

    @staticmethod
    async def get_by_email(
        db,
        email:str):

        result = await db.execute(
            select(User).where(User.email == email))

        return result.scalar_one_or_none()
