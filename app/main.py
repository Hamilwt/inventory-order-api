from fastapi import FastAPI
from app.core.config import settings

# Bulletproof direct imports
from app.api.products import router as products_router
from app.api.orders import router as orders_router

# 1. Import Scalar
from scalar_fastapi import get_scalar_api_reference 

# 2. Disable the default Swagger and ReDoc UI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A professional backend API for managing inventory and orders.",
    docs_url=None, 
    redoc_url=None 
)

# 3. Attach the routers
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

# 4. Serve the beautiful Scalar UI at our /docs route
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )