from pydantic import BaseModel, EmailStr
from bson import ObjectId

class User(BaseModel):
    id: str = None
    email: EmailStr
    password: str
    fullname: str
    admin: bool = False
    verifyPassword: str
    class Config:
        json_encoders = {ObjectId: str}