# app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field, validator
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import User  # Import the User model
from typing import List

router = APIRouter()

class SignInRequest(BaseModel):
    fullname: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    verifyPassword: str = Field(..., description="Password verification")

    @validator('verifyPassword')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

async def get_database() -> AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db

@router.post("/signin")
async def sign_in(request: SignInRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if the user already exists
    existing_user = db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="User  already exists")

    # Create a new user
    new_user = {
        "fullname": request.fullname,
        "email": request.email,
        "password": request.password  # In a real application, make sure to hash the password
    }

    try:
        db.users.insert_one(new_user)
        return {"message": "User  created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")