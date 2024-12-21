# app/models/cart.py
from pydantic import BaseModel, Field
from typing import Dict, Any
from typing import List

class CartItem(BaseModel):
    item_id: str = Field(..., description="The ID of the item to add to the cart")
    quantity: int = Field(..., description="The quantity of the item to add")

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]

class Cart(BaseModel):
    items: Dict[str, CartItem]  # Dictionary of items in the cart, keyed by item ID
    totalQty: int                # Total quantity of items in the cart
    totalPrice: float            # Total price of the cart
    userId: str                  # User ID associated with the cart

    class Config:
        # Allow population of the model from MongoDB documents
        orm_mode = True
    
