from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models import Base

# --- BEGIN ADDED DEBUG ---
print(f"DEBUG [database.py]: Initializing engine with DATABASE_URL: '{settings.DATABASE_URL}'")
# --- END ADDED DEBUG ---
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 