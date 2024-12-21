# app/routers/users.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.database import get_db
from passlib.context import CryptContext
from app.models.cart import Cart
from app.modules.ensure_authenticated import ensure_authenticated
from pydantic import BaseModel, EmailStr, Field, validator
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_database()->AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db

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

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User 's email")
    password: str = Field(..., description="User 's password")

async def get_database() -> AsyncIOMotorDatabase:
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    return db

@router.post("/signin")
async def sign_in(request: SignInRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if the user already exists
    existing_user = await db.users.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(status_code=409, detail="User  already exists")

    # Create a new user
    new_user = {
        "fullname": request.fullname,
        "email": request.email,
        "password": request.password  # In a real application, make sure to hash the password
    }

    try:
        await db.users.insert_one(new_user)
        return {"message": "User  created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @router.post("/login")
# async def login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
#     email = request.email
#     password = request.password
#
#     # Check if the user exists
#     user = await db.users.find_one({"email": email})
#     if not user:
#         raise HTTPException(status_code=403, detail="Incorrect email or password")
#
#     # Verify the password
#     if not verify_password(password, user['password']):  # Assuming you have a function to verify passwords
#         raise HTTPException(status_code=403, detail="Incorrect email or password")
#
#     # Create JWT token
#     token = jwt.encode(
#         {"email": email, "exp": datetime.utcnow() + timedelta(days=7)},
#         "your_secret_key",  # Replace with your actual secret key
#         algorithm="HS256"
#     )
#
#     return {
#         "user_token": {
#             "user_id": str(user['_id']),  # Convert ObjectId to string
#             "user_name": user['fullname'],
#             "token": token,
#             "expire_in": "7d"
#         }
#     }

@router.get("/{user_id}/cart", response_model=Cart)
async def get_cart(user_id: str, current_user: User = Depends(ensure_authenticated)):
    db = get_db()

    # Fetch the cart for the user
    cart = await Cart.get_cart_by_user_id(user_id)

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

@router.post("/{user_id}/cart", response_model=Cart)
async def update_cart(user_id: str, cart_data: Cart, current_user: User = Depends(ensure_authenticated)):
    db = get_db()

    # Fetch the existing cart for the user
    existing_cart = await Cart.get_cart_by_user_id(user_id)

    if existing_cart:
        # Update the existing cart
        updated_cart = await Cart.update_cart_by_user_id(user_id, cart_data)
        return updated_cart
    else:
        # Create a new cart if none exists
        new_cart = await Cart.create_cart(cart_data)
        return new_cart