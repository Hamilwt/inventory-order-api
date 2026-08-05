from fastapi import FastAPI
from app.core.config import settings

# Bulletproof direct imports
from app.api.products import router as products_router
from app.api.orders import router as orders_router

# The standard, out-of-the-box FastAPI setup
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A professional backend API for managing inventory and orders."
)

# Attach the routers
app.include_router(products_router)
app.include_router(orders_router)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Check if the API is running successfully.
    """
    return {
        "status": "ok", 
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION
    }