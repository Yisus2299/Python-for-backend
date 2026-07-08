# here will be the valitradion with Pydantic models
# Schemas checks if the JSON is safe and sound, it's what the user will see:
from pydantic import BaseModel
from typing import List

#Response: it's what the server sends to the client (frontend). it's what the server responds
#Model: save it into the DataBase
#Create: it validates the data that gets (Backend). Its what you ask to the server

# examples: 
# create = { "email": "a@a.com", "password": "1234" }
# model = UserModel(email="a@a.com", hashed_password="hash_encriptado")
# response = { "id": 1, "email": "a@a.com", "is_active": true }


# the base to receive data from Frontend
class CategoryCreate(BaseModel):
    name: str

# the base to respond back to the frontend
class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True #this class config only goes on responses

class ProductCreate(BaseModel): #with this we will use the POST and PUT method
    name: str
    price: float
    is_offer: bool = False
    category_id: int #we force the frontend to move data to one category
    
class ProductResponse(BaseModel): #ProductResponse makes what the user wants goes through the filter we created
    id: int #and it makes sure it only shows 4 fields
    name: str
    price: float
    is_offer: bool
    category_id: int | None = None #we insert the schema inside here
    category: CategoryResponse | None = None

    class Config:
        from_attributes = True

# now, we will create the user schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True
        
# the base what the client will receive at the moment he sing in with the login:
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    created_at: str
    
    class Config:
        from_attributes = True