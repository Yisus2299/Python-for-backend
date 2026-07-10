# we have these two: 
# 1- passlib[bcrypt]: turns passwords into a secret hash before saving it into the clouds
# 2- PyJWT: Tool that will generate JTW Tokens when the user sings in successfully

import jwt
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer # this means: this API requires a security token
from fastapi import HTTPException, Depends
import bcrypt
from dotenv import load_dotenv

#secret server configurations 
SECRET_KEY = os.environ.get("JWT_SECRET", "Alekk070903")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# we load the .env
load_dotenv()

# this line tells FastAPI that looks for the token in the route /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- NEW PASSWORD FUNCTIONS---

# Function 1: it receives the clean password and send back trillions of encrypt text
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Function 2: it compares the plain password which the user writes on the login
# with the hash we got, it will send TRUE or FALSE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

#Function 3: It generates the packet token with the user information
def create_access_token(data: str):
    to_encode = data.copy()
    # we calculate the exact expiration hour using the UTC time zone
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # we put the expiration to the data packet ('exp')
    to_encode.update({"exp": expire})
    # we sing and create the JWT Token String
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function 4: this will protect the routes that we will implement in Products.py
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # We decodificate the token using our secret password
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # We extract the email we save in the Login
        if email is None:
            raise credentials_exception
        return email # we get the email back if all goes fine
    except jwt.PyJWTError:
        raise credentials_exception