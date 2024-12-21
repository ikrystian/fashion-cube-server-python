# app/modules/ensure_authenticated.py
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.user import User
from app.database import get_db

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ALGORITHM = "HS256"

async def ensure_authenticated(token: str = Security(oauth2_scheme)):
    db = get_db()
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Fetch the user from the database
        user = await User.get_user_by_email(email)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user