# app/models/order.py
from pydantic import BaseModel
from typing import Dict, Any
from app.database import get_db

class Order(BaseModel):
    userId: str
    cartId: str
    totalAmount: float
    items: Dict[str, Any]  # This can be a dictionary representing the items in the order
    status: str = "pending"  # Default status

    class Config:
        from_attributes = True

async def create_order(order_data: Order):
    db = get_db()
    order = await db.orders.insert_one(order_data.dict())
    return order_data