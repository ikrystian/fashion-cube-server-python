# app/models/product.py
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List

class Product(BaseModel):
    id: Optional[str] = None  # This will be set to None when creating a new product
    imagePath: str
    title: str
    description: str
    department: str
    category: str
    price: float
    color: str
    size: str
    quantity: int
    date: int  # You may want to consider using a more appropriate type for date

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to string for JSON serialization