from repository.user import UserRepository
from schema.user import UserCreate, UserUpdate, UserResponse
from services.cart import CartService
from tasks.email_task import send_welcome_email
from utils.cache import CacheManager

class UserService:

    @staticmethod
    async def get_all(
        db):

        users =await  UserRepository.get_all(db)

        return users


    @staticmethod
    async def create(
        user: UserCreate,
        db):

        created = await UserRepository.create(user,db)

        user_data = await UserRepository.get_by_mail(db,user.email)

        await CartService.create_cart(db,user_data.id)

        send_welcome_email.delay(user.email)

        return created

    @staticmethod
    async def get_by_id(
        id,
        db):

        cached_key = f"user:{id}"

        cached = await CacheManager.get(cached_key)

        if cached:
            return UserResponse.model_validate_json(cached)

        me = await UserRepository.get_by_id(id,db)

        res = UserResponse.model_validate(me)

        await CacheManager.set(
            cached_key,
            res.model_dump_json(),
            ttl=300)

        return me

    @staticmethod
    async def delete(
        user_id: int,
        db):

        cached_key = f"user:{user_id}"
        deleted = await UserRepository.delete(user_id,db)

        await CacheManager.delete(cached_key)
        return deleted

    @staticmethod
    async def update_user(
    user_id: int,
        user_data: UserUpdate,
        db):

        cached_key = f"user:{user_id}"
        updated = await UserRepository.update(user_id,user_data,db)

        await CacheManager.delete(cached_key)
        return updated
