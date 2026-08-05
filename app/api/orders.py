from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse

# Create a router instance for orders
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """
    Place a new order, securely lock in prices, and deduct inventory.
    """
    # 1. Create the top-level order first
    new_order = Order(customer_id=order_in.customer_id, status="completed")
    db.add(new_order)
    db.flush() # Gets the order ID from the database without fully saving yet

    # 2. Process each item the customer wants to buy
    for item in order_in.items:
        # Look up the product in the database
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        # Check 1: Does the product exist?
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found.")
        
        # Check 2: Do we have enough stock?
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock for {product.name}. Only {product.stock_quantity} left."
            )

        # 3. Create the Order Item (Securely grabbing the price from the DB)
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_time_of_order=product.price # SECURITY: Overriding anything the user sent
        )
        db.add(order_item)

        # 4. Deduct the purchased amount from the inventory
        product.stock_quantity -= item.quantity

    # 5. Commit the transaction (All or Nothing)
    db.commit()
    db.refresh(new_order)
    
    return new_order