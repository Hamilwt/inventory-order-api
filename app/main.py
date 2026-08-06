import os
import sentry_sdk
from fastapi import FastAPI
from app.core.config import settings

# 1. Bulletproof direct imports
from app.api.products import router as products_router
from app.api.orders import router as orders_router
from scalar_fastapi import get_scalar_api_reference 

# 2. Initialize Sentry (Hardcoded for testing)
sentry_sdk.init(
    dsn="https://eb41bd190d33d51bbc6a867de8bd838f@o4511830720708608.ingest.us.sentry.io/4511862472769536",
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# 3. Initialize FastAPI and disable default Swagger/ReDoc
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A professional backend API for managing inventory and orders.",
    docs_url=None, 
    redoc_url=None 
)

# 4. Attach the routers
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

# 5. Serve the beautiful Scalar UI
@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

# --- Sentry Debug Route ---
@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0