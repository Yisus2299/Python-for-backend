# this will be the ORM; it saves the whole object in the database; we create the table here and what it'll has inside

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

#We'll add some new tables:

class OrderItemModel(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(String, default=1)
    price_at_purchase = Column(Float, nullable=False)
    
    product = relationship("ProductModel")
    
class OrderModel(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(datetime, default=lambda: datetime.now(timezone.utc))
    
    #relationships
    
    user = relationship("UserModel")
    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")

OrderItemModel.order = relationship("OrderModel", back_populates="items")

class CategoryModel(Base): #we create a new table called Categories and its above products
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique= True, index=True) #Unique = means "there won't be a repeated name"
    products = relationship("ProductModel", back_populates="category") #this new line connects ProductModel witn CategoryModel. This is for you to access to a category if you're in a product 

class ProductModel(Base):
    __tablename__ = "products" #when we create the table it will has the name "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("CategoryModel", back_populates="products") # and from a category you can access to all it's products

# Let's start with JWT:
# now let's create UserModel for saving it into test.db

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)