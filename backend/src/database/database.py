"""Database connection and session setup for Todo application."""

from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

# For PostgreSQL (Neon), we'll use the async engine approach but start with sync
engine = create_engine(DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session