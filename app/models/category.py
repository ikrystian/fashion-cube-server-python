from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Category(BaseModel):
    id: Optional[str] = None  # This will be set to None when creating a new category
    categoryName: str

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to string for JSON serialization