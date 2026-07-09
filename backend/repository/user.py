from sqlalchemy import select


from models.user import User
from schema.user import UserCreate, UserUpdate

from utils.password_hasher import PasswordHasher

class UserRepository:

    @staticmethod
    async def get_all(db):
        query = await db.execute(select(User))

        users = query.scalars().all()

        return users

    @staticmethod
    async def create(user: UserCreate,db):
        query = await db.execute(select(User.email).where(User.email == user.email))
        email = query.scalar_one_or_none()
        if email:
            raise ValueError(f'User with {email} already Exists')


        user_data = User(
            name = user.name,
            email = user.email,
            hashed_password = PasswordHasher.create_hash(user.hashed_password))
        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)
        return user_data

    @staticmethod
    async def get_by_id(
        id,db):
        query = await db.execute(select(User).where(User.id == id, User.isDeleted == False))
        user = query.scalar_one_or_none()
        return user

    @staticmethod
    async def delete(user_id, db):
        query = await db.execute(select(User).where(User.id == user_id , User.isDeleted == False))
        user = query.scalar_one_or_none()
        if user:
            user.isDeleted = True
            await db.commit()
            await db.refresh(user)
            return user
        return None

    @staticmethod
    async def get_by_mail(
        db,
        email: str):
        query = await db.execute(select(User).where(User.email == email))
        user = query.scalar_one_or_none()
        return user

    @staticmethod
    async def get_mail_by_id(
        db,
        user_id: int):
        query = await db.execute(select(User.email).where(User.id == user_id))
        user = query.scalar_one()
        return user

    @staticmethod
    async def update(
    user_id: int,user_data: UserUpdate,
                      db):
        query = await db.execute(select(User).where(User.id == user_id, User.isDeleted == False))
        user = query.scalar_one_or_none()

        if user:
            user.name = user_data.name
            user.email = user_data.email
            await db.commit()
            await db.refresh(user)
            return user
        return None
