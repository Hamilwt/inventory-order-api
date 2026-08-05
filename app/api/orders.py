from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

# 1. CREATE ORDER (POST)
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """Place a new order, securely lock in prices, and deduct inventory."""
    new_order = Order(customer_id=order_in.customer_id, status="pending")
    db.add(new_order)
    db.flush() 

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found.")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}.")

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_time_of_order=product.price 
        )
        db.add(order_item)
        product.stock_quantity -= item.quantity

    db.commit()
    db.refresh(new_order)
    return new_order

# 2. GET ALL ORDERS (GET)
@router.get("/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all orders."""
    return db.query(Order).offset(skip).limit(limit).all()

# 3. GET SINGLE ORDER (GET /{id})
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# 4. UPDATE ORDER STATUS (PATCH /{id})
@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    """Update the shipping status of an order (e.g., 'shipped', 'cancelled')."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order

# 5. DELETE ORDER (DELETE /{id})
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Cancel and delete an order."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return None