# here will be the valitradion with Pydantic models
# Schemas checks if the JSON is safe and sound, it's what the user will see:
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

#Response: it's what the server sends to the client (frontend). it's what the server responds
#Model: save it into the DataBase
#Create: it validates the data that gets (Backend). Its what you ask to the server

# examples: 
# create = { "email": "a@a.com", "password": "1234" }
# model = UserModel(email="a@a.com", hashed_password="hash_encriptado")
# response = { "id": 1, "email": "a@a.com", "is_active": true }

# users and tokens

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
        
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# categories

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        
# products

class ProductCreate(BaseModel):
    name: str
    price: float
    is_offer: bool = False
    category_id: int
    
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool
    category_id: Optional[int] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

# New orders

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class ProductInOrder(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    price_at_purchase: float
    product: ProductInOrder
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime 
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
    