# app/routers/categories.py
from fastapi import APIRouter, HTTPException
from app.models.category import Category
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=Category)
async def create_category(category: Category):
    db = get_db()
    result = db.categories.insert_one(category.dict())
    category.id = str(result.inserted_id)  # Set the ID of the created category
    return category

@router.get("/")
async def get_categories():
    db = get_db()
    categories = list(db.categories.find())
    for category in categories:
        category['_id'] = str(category['_id'])  # Convert ObjectId to string
    return {"categories": categories}