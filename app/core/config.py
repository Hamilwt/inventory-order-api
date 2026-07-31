from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventory & Order Management API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str

    # Modern Pydantic v2 configuration syntax
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Create a single instance to use throughout the app
settings = Settings()