# app/routers/filter.py
from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, List, Optional

router = APIRouter()

async def get_database() -> AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db

def generate_filter_result_array(products: List[Dict], key: str) -> List[str]:
    """Generate a unique list of values for a given key from the product list."""
    return list(set(product[key] for product in products if key in product))

@router.get("/")
async def filter_products(query: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = {}

    try:
        # Filter by department
        departments = await db.products.find({"department": {"$regex": query, "$options": "i"}}).to_list(length=None)
        if departments:
            result['department'] = generate_filter_result_array(departments, 'department')

        # Filter by category
        categories = await db.products.find({"category": {"$regex": query, "$options": "i"}}).to_list(length=None)
        if categories:
            result['category'] = generate_filter_result_array(categories, 'category')

        # Filter by title
        titles = await db.products.find({"title": {"$regex": query, "$options": "i"}}).to_list(length=None)
        if titles:
            result['title'] = generate_filter_result_array(titles, 'title')

        if result:
            return {"filter": result}
        else:
            raise HTTPException(status_code=404, detail="No products exist")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")