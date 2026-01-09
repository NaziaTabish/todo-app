"""Authentication API endpoints for Todo application."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import timedelta
from ..database.database import get_session
from ..models.user import User, UserCreate, UserRead
from ..services.user_service import UserService
from typing import Dict

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if user with email already exists
    existing_user = UserService.get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Check if username already exists
    existing_username = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )

    # Create the new user
    db_user = UserService.create_user(session, user_create)
    return db_user


@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    """Authenticate user and return access token."""
    user = UserService.authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=UserService.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserService.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }


@router.post("/logout")
def logout():
    """Logout user (client-side token invalidation)."""
    # In a stateless JWT system, logout is typically handled client-side
    # by removing the token from storage
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserRead)
def get_current_user(current_user: UserRead = Depends(get_current_active_user)):
    """Get current authenticated user's information."""
    return current_user