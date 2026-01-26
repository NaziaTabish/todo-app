"""Main application entry point for Todo application."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from .database.database import engine
from .api.auth import router as auth_router
from .api.v1.users import router as users_router
from .api.v1.tasks import router as tasks_router
from .models.user import User
from .models.task import Task
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler."""
    logger.info("Starting up application...")

    # Create database tables
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

    yield

    logger.info("Shutting down application...")

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="API for Todo application with authentication",
    version="0.0.1",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tasks_router, prefix="/api/users", tags=["tasks"])

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Welcome to Todo API"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)