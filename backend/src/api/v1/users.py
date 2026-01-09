"""User management API endpoints for Todo application."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ...database.database import get_session
from ...models.user import User, UserCreate, UserRead, UserUpdate
from ...services.user_service import UserService

router = APIRouter()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, session: Session = Depends(get_session)):
    """Get user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):
    """Update user information."""
    updated_user = UserService.update_user(session, user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: str, session: Session = Depends(get_session)):
    """Delete a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # For soft delete, we'll deactivate the user
    user.is_active = False
    session.add(user)
    session.commit()

    return {"message": "User deactivated successfully"}