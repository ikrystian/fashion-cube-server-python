# app/models/department.py
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Department(BaseModel):
    id: Optional[str] = None  # This will be set to None when creating a new department
    departmentName: str
    categories: str  # You may want to consider using a list of categories instead

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to string for JSON serialization