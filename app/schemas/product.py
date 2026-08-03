from pydantic import BaseModel, ConfigDict
from typing import Optional

# Base properties shared across all product actions
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0

# Schema for when a user creates a product (inherits all base properties)
class ProductCreate(ProductBase):
    pass

# Schema for what the API sends back to the user
class ProductResponse(ProductBase):
    id: int

    # Modern Pydantic v2 configuration to allow reading from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)