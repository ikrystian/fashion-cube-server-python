# app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field, validator
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import User  # Import the User model
from typing import List
import jwt
from datetime import datetime, timedelta
from app.configs.jwt_config import secret
router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User 's email")
    password: str = Field(..., description="User 's password")

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

async def verify_password(password, userPassword):
    return true

@router.post("/login")
async def login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    email = request.email
    password = request.password

    # Check if the user exists
    user =  db.users.find_one({"username": email})
    if not user:
        raise HTTPException(status_code=403, detail="Incorrect email or ")

    # Verify the password
    if not verify_password(password, user['password']):
        raise HTTPException(status_code=403, detail="Incorrect password")

    # Create JWT token
    token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(days=7)},
        secret,  # Replace with your actual secret key
        algorithm="HS256"
    )

    return {
        "user_token": {
            "user_id": str(user['_id']),  # Convert ObjectId to string
            "user_name": user['fullname'],
            "token": token,
            "expire_in": "7d"
        }
    }