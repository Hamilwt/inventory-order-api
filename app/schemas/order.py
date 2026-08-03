from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

# What the user sends us to create a single item in their cart
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    # Notice: No price field! We calculate that securely on the backend.

# What the user sends us to checkout
class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItemCreate]

# What we send back to the user to confirm their item
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_time_of_order: float

    model_config = ConfigDict(from_attributes=True)

# What we send back to the user for the full receipt
class OrderResponse(BaseModel):
    id: int
    customer_id: str
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)