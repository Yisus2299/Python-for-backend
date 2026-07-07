# we're trying to avoid to turn main.py into a 3k lines of code doc
# so in order to avoid that, we've created Router's Folder and inside it's this file
# here we'll bring everything and modify all the Endpoints for using them into Main.py in a easier and shorter way

# we import first fastapi and sql for the database
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# now we need to import what we have in the rest of our files
# we use ".." to go outside the folder, it's like "../"
from database import get_db
from schemas import ProductCreate, ProductResponse
from models import ProductModel

# we implement get_current_user from auth_utils
from auth_utils import get_current_user

# 1- we rename and start APIRouter
# we add a 'prefix' to avoid to type "/produtcs" in every single route
# we add 'tags to make Swagger to be organized under Produtc's section
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# remember: 
# Depends = Before executing, get the session from ..
# Example: (Depends(get_db)) = before executing, get the database session and check

#2- we move all Endpoints changing their @app for @router instead

@router.get("", response_model=list[ProductResponse]) # this is the same as "/produtcs"
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    return products

@router.get("/{product_id}", response_model= ProductResponse) # this is the same as "/products/{product_id}""
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not Found")
    return product

# HERE, we will implement get_current_user to protect the product creations
@router.post("", status_code=201, response_model= ProductResponse) # this is the same as "/products" but we're creating it with POST and 200/201 means all went 10/10
def create_product(product_in: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_product = ProductModel (
        name = product_in.name,
        price = product_in.price,
        is_offer = product_in.is_offer,
        category_id= product_in.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not updated:
        raise HTTPException(status_code=404, detail="Product can't be updated")
    updated.name = product_in.name
    updated.price = product_in.price
    updated.is_offer = product_in.is_offer
    updated.category_id = product_in.category_id
    db.commit()
    db.refresh(updated)
    return updated

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    deleted = db.query(ProductModel).filter(ProductModel.id==product_id).first()
    if not deleted:
        raise HTTPException(status_code=404, detail="Product can't be deleted")
    
    db.delete(deleted)
    db.commit()
    return None