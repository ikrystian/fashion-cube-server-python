# app/routers/products.py
from fastapi import APIRouter, HTTPException
from app.models.product import Product
from app.database import get_db
from bson import ObjectId

router = APIRouter()
db = get_db()

@router.get("/")
async def get_products():

    products = list(db.products.find())
    for product in products:
        product['_id'] = str(product['_id'])
    return {"products": products}

@router.get("/{product_id}")
async def get_product(product_id: str):
    product = db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product['_id'] = str(product['_id'])
    return product