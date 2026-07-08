# (we might need to install: pip install "passlib[bcrypt]" PyJWT)
# this is the satelite will handle the Register of users

from json import JSONDecodeError
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse, TokenResponse
from models import UserModel
from auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth", #this means (/auth/)
    tags=["Authentication"] #this creates a Swagger tag with this name
)

# ENDPOINTS: REGISTER, LOGIN, POST

# for REGISTER users (sign up)
@router.post("/register", status_code=201, response_model=UserResponse)
def register_user(user_in: UserCreate,db: Session = Depends(get_db)):
    # verify if there is an existing user:
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # we cypher the password before saving it
    encrypted_pass = hash_password(user_in.password)
    # now we save the user with the encrypted password
    new_user = UserModel(
        email = user_in.email,
        hashed_password=encrypted_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# for Login users (sign in):
@router.post("/login", status_code=200, response_model=TokenResponse)
async def logging_user(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("content-type", "")
    email = None
    password = None

    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        email = form.get("username") or form.get("email")
        password = form.get("password")
    else:
        try:
            data = await request.json()
        except JSONDecodeError:
            data = {}
        email = data.get("email") or data.get("username")
        password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=422, detail="email and password are required")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    is_valid = verify_password(password, user.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

    


    

