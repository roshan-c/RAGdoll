#!/usr/bin/env python3
"""
Database initialization script for RAGdoll Docker setup.
This script creates the necessary tables when the container starts.
"""

import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Add the app directory to Python path
sys.path.append('/app')

from app.db.models import Base
from app.core.database import engine

def wait_for_db(max_retries=30, delay=2):
    """Wait for database to be ready."""
    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            return True
        except OperationalError:
            print(f"Database not ready, attempt {attempt + 1}/{max_retries}. Waiting {delay} seconds...")
            time.sleep(delay)
    
    print("Database failed to become ready after maximum retries.")
    return False

def create_tables():
    """Create database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Initializing RAGdoll database...")
    
    if wait_for_db():
        if create_tables():
            print("Database initialization completed successfully!")
            sys.exit(0)
        else:
            print("Failed to create tables!")
            sys.exit(1)
    else:
        print("Failed to connect to database!")
        sys.exit(1) 