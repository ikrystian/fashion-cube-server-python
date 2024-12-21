# app/database.py
from app.configs.mongo_config import db

def get_db():
    return db

from app.models.cart import Cart, CartItem


async def add_item_to_cart(user_id: str, item: CartItem):
    # Find the user's cart and update it
    result = await db.carts.update_one(
        {"user_id": user_id},
        {"$addToSet": {"items": item.dict()}},  # Use $addToSet to avoid duplicates
        upsert=True  # Create a new cart if it doesn't exist
    )
    return result


class CartDB:
    @staticmethod
    async def get_cart_by_user_id(user_id: str):
        db = get_db()
        cart = await db.carts.find_one({"userId": user_id})
        return cart

    @staticmethod
    async def update_cart_by_user_id(user_id: str, cart_data: Cart):
        db = get_db()
        updated_cart = await db.carts.find_one_and_update(
            {"userId": user_id},
            {"$set": cart_data.dict()},
            return_document=True
        )
        return updated_cart

    @staticmethod
    async def create_cart(cart_data: Cart):
        db = get_db()
        cart = await db.carts.insert_one(cart_data.dict())
        return cart_data