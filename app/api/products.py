from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

# 1. CREATE (POST)
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the inventory."""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 2. READ ALL (GET)
@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of all products."""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# 3. READ SINGLE (GET /{id})
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific product by its ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 4. UPDATE (PUT /{id})
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_product: ProductCreate, db: Session = Depends(get_db)):
    """Update a product's name, description, price, or stock."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update the fields
    for key, value in updated_product.model_dump().items():
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return product

# 5. DELETE (DELETE /{id})
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Remove a product from the database."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return None