# app/models/cart.py
from pydantic import BaseModel, Field
from typing import Dict, Any

class CartItem(BaseModel):
    item: Dict[str, Any]  # This can be a dictionary representing the product
    qty: int              # Quantity of the item
    price: float          # Total price for this item

class Cart(BaseModel):
    items: Dict[str, CartItem]  # Dictionary of items in the cart, keyed by item ID
    totalQty: int                # Total quantity of items in the cart
    totalPrice: float            # Total price of the cart
    userId: str                  # User ID associated with the cart

    class Config:
        # Allow population of the model from MongoDB documents
        from_attributes = True

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