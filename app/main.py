from fastapi import FastAPI
from app.core.config import settings
from app.api import products

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A professional backend API for managing inventory and orders."
)

app.include_router(products.router)

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