# app/routers/variants.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.variant import Variant  # Assuming you have a Variant model
from app.database import get_db
from app.modules.ensure_authenticated import ensure_authenticated
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId  # Import ObjectId from bson
from app.models.user import User  # Import the User model

router = APIRouter()

async def get_database()->AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db


@router.get("/")
async def get_variants():
    db = get_db()
    variants = list(db.variants.find())
    for variant in variants:
        variant['_id'] = str(variant['_id'])  # Convert ObjectId to string
    return {"variants": variants}

@router.post("/", response_model=Variant)
async def create_variant(variant: Variant):
    db = get_db()
    result = db.variants.insert_one(variant.dict())
    variant.id = str(result.inserted_id)  # Set the ID of the created variant
    return variant

@router.get("/{variant_id}")
async def get_variant(variant_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    variant =  db.variants.find_one({"_id": ObjectId(variant_id)})
    
    if not variant:
        raise HTTPException(status_code=404, detail="Product not found")
    
    variant['_id'] = str(variant['_id'])  # Convert ObjectId to string for JSON serialization
    return variant
