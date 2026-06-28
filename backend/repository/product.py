
from sqlalchemy import select
from models.product import Product
from schema.product import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

class ProductRepository:

    @staticmethod
    async def products(db):
        query = await db.execute(select(Product))
        products = query.scalars().all()

        return products

    @staticmethod
    async def get_by_id(db,id:int):
        query = await db.execute(select(Product).where(Product.id == id))
        products = query.scalar_one_or_none()

        return products

    @staticmethod
    async def create_product(db, product: ProductCreate):
        data = product.model_dump()
        data["sku"] = str(uuid.uuid4())
        data["created_at"] = datetime.now()
        db_product = Product(**data)
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    @staticmethod
    async def update_product(db: Session, prod_id: int, product_update_data: ProductUpdate):
        query = await db.execute(select(Product).where(Product.id == prod_id))
        db_product = query.scalar_one_or_none()
        if db_product:
            for key, value in product_update_data.model_dump(exclude_unset=True).items():
                setattr(db_product, key, value)
            await db.commit()
            await db.refresh(db_product)
        return db_product

    @staticmethod
    async def delete_product(db: Session, prod_id: int):
        query = await db.execute(select(Product).where(Product.id == prod_id))
        db_product = query.scalar_one_or_none()
        if db_product:
            await db.delete(db_product)
            await db.commit()
            return prod_id
        return None
