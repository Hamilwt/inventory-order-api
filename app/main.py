from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api import products

# 1. Turn off the default ReDoc so we can build our own
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A professional backend API for managing inventory and orders.",
    redoc_url=None  
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

# 2. Build the custom, enhanced ReDoc UI
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Import the Inter font for a modern, premium look -->
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        </style>
    </head>
    <body>
        <!-- Inject ReDoc with custom theme settings -->
        <redoc spec-url="/openapi.json" hide-download-button options='{
            "theme": {
                "colors": {
                    "primary": { "main": "#6366f1" },
                    "text": { "primary": "#1f2937" }
                },
                "typography": {
                    "fontFamily": "Inter, sans-serif",
                    "headings": {
                        "fontFamily": "Inter, sans-serif",
                        "fontWeight": "700"
                    }
                },
                "sidebar": {
                    "backgroundColor": "#f8fafc"
                }
            }
        }'></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)