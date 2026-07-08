from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import OrderModel, OrderItemModel, ProductModel, UserModel
from schemas import OrderCreate, OrderResponse
from auth_utils import get_current_user

router = APIRouter(
    prefix="/orders",
    tags= ["Orders"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    # look for the logged user in the database using the email we took from Token
    user = db.query(UserModel).filter(UserModel.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    # crear the main order:
    new_order = OrderModel(user_id=user.id)
    db.add(new_order)
    db.flush() # it generates the Order ID into the Database without confirm
    
    # we process every single product that has been sent to the Frontend
    for item in order_in.items:
        # we look for the product in the database for making sure it does exist and getting it's real price
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        if not product:
            db.rollback() # we cancel everything if a product doesn't exist for avoiding corrupt data
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID{item.product_id} not found"
            )
            
            # we create the detail about the order with the locked-in-price at the purchase time:
        order_item = OrderItemModel(
            order_id = new_order.id,
            product_id = product.id,
            quantity = item.quantity,
            price_at_purchase = product.price
        )
        db.add(order_item)
        
        # we save definitely all changes in SQLite
    db.commit()
    db.refresh(new_order)
        
    return new_order
    
@router.get("", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user)
):
    # we look for the user thanks to the email
    user = db.query(UserModel).filter(UserModel.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # bring the user orders
    orders = db.query(OrderModel).filter(OrderModel.user_id == user.id).all()
    return orders