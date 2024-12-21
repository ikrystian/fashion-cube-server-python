# app/routers/departments.py
from fastapi import APIRouter, HTTPException
from app.models.department import Department
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=Department)
async def create_department(department: Department):
    db = get_db()
    result = db.departments.insert_one(department.dict())
    department.id = str(result.inserted_id)  # Set the ID of the created department
    return department

@router.get("/")
async def get_departments():
    db = get_db()
    departments = list(db.departments.find())
    for department in departments:
        department['_id'] = str(department['_id'])  # Convert ObjectId to string
    return {"departments": departments}