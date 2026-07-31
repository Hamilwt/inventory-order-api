from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# The Engine is the core interface to the database
engine = create_engine(settings.DATABASE_URL)

# SessionLocal represents a single database connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The modern SQLAlchemy 2.0 way to define the base model
class Base(DeclarativeBase):
    pass

# Dependency to give each API request its own database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()