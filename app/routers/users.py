# app/routers/users.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.database import CartDB, get_db, add_item_to_cart
from passlib.context import CryptContext
from app.models.cart import Cart, CartItem, CartResponse
from app.modules.ensure_authenticated import ensure_authenticated
from pydantic import BaseModel, EmailStr, Field, validator
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class UserLoginRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    credential: UserLoginRequest

@router.post("/signin", response_model=User )
async def create_user(user: User):
    db = get_db()
    
    existing_user = db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="User  already exists")
    
    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password = pwd_context.hash(user.password),
        verifyPassword=user.verifyPassword 
    )
    user_dict = new_user.dict(exclude={"verifyPassword"}) 

    db.users.insert_one(user_dict)
    return user

@router.post("/login")
async def login(login_request: LoginRequest):
    db = get_db()
    user = db.users.find_one({"email": login_request.credential.email})
    if not user or not verify_password(login_request.credential.password, user['password']):
        raise HTTPException(status_code=403, detail="Incorrect email or password")
    
    token = jwt.encode(
        {"email": login_request.credential.email, "exp": datetime.utcnow() + timedelta(days=7)},
        "your_secret_key",  # Replace with your actual secret key
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
        

async def get_database()->AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db

@router.get("/{user_id}/cart", response_model=Cart)
async def get_cart(user_id: str):
    return ''
    db = get_db()

    # Fetch the cart for the user
    cart = await CartDB.get_cart_by_user_id(user_id)

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

@router.post("/{user_id}/cart", response_model=CartResponse)
async def add_to_cart(product_id, user_id):
    # Add the item to the user's cart
    result = await add_item_to_cart(user_id, {"item_id": product_id, "quantity": 1})
    
    if result.modified_count == 0 and result.upserted_id is None:
        raise HTTPException(status_code=400, detail="Failed to add item to cart")

    # Return the updated cart (for simplicity, we return the item added)
    return CartResponse(user_id=user_id, items=[item])