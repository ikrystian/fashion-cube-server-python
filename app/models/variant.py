# app/models/variant.py
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Variant(BaseModel):
    id: Optional[str] = None  # This will be set to None when creating a new variant
    productID: str
    imagePath: str
    color: str
    size: str
    quantity: int

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to string for JSON serialization