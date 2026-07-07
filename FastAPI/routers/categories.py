from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import CategoryCreate, CategoryResponse
from models import CategoryModel

# we start APIRouter for the categories
router = APIRouter(
    prefix="/categories", #this means (/categories/)
    tags=["Categories"]
)

# Endpoints for Creating a category (POST)
# we create an Endpoint to List all the categories
@router.get("", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    all_categories = db.query(CategoryModel).all()
    return all_categories

@router.get("/{category_id}", status_code=201, response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category doesn't exist")
    return category

@router.post("", status_code=201, response_model=CategoryResponse)
def create_category(category_in: CategoryCreate ,db: Session = Depends(get_db)):
    # we check if there isn't an existing a category with the same name
    existing_category = db.query(CategoryModel).filter(CategoryModel.name == category_in.name).first() # remember, db.query is for asking questions to de database
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    # if not, we create the ORM model
    new_category = CategoryModel(name=category_in.name)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
    
@router.put("/{category_id}", status_code=200, response_model=CategoryResponse)
def update_category(category_in: CategoryCreate, category_id: int,db: Session = Depends(get_db)):
    update = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not update:
        raise HTTPException(status_code=404, detail="Category not Found")
    
    update.name = category_in.name
        
    db.commit()
    db.refresh(update)
    return update

@router.delete("/{category_id}") # here we don't use either response_model or anything
def delete_category(category_id: int, db: Session = Depends(get_db)):
    to_delete = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not to_delete:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(to_delete)
    db.commit()
    return{"message": f"{category_id} was deleted succesfully"}