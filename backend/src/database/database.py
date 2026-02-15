"""Database connection and session setup for Todo application."""

from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
# Load environment variables
load_dotenv(override=True)

# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

# Ensure postgresql+psycopg is used for consistency with psycopg 3
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Fallback to SQLite if Postgres is configured but we want to force local dev or if env var is stuck
if DATABASE_URL.startswith("postgresql") and os.name == 'nt':
    # On Windows without explicit psycopg2, default back to sqlite to ensure startup
    DATABASE_URL = "sqlite:///./todoapp.db"

# For PostgreSQL (Neon/Supabase), we add pool_pre_ping to handle stale connections
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300, # Recycle connections every 5 minutes
)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session