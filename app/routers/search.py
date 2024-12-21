from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

async def get_database()->AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db

@router.get("/search")
async def global_search(query: str, db: AsyncIOMotorDatabase = Depends(get_database)):

    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    results = {
        "products": [],
    }

    try:
        # Search in the variants collection
         for product in db.products.find({"title": {"$regex": query, "$options": "i"}}):
            product['_id'] = str(product['_id'])  # Convert ObjectId to string for JSON serialization
            results["products"].append(product)


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    return results