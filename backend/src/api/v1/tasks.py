"""Task management API endpoints for Todo application."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from ...database.database import get_session
from ...models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ...models.user import User
from ...services.task_service import TaskService
from ...api.deps import get_current_active_user

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    status: str = Query("all", description="Filter tasks by completion status: all, pending, completed"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip")
):
    """Get all tasks for a specific user with optional filtering."""
    # Ensure user can only access their own tasks
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    tasks = TaskService.get_tasks_by_user(session, user_id, status, limit, offset)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: str,
    task_create: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task for a user."""
    # Ensure user can only create tasks for themselves
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Override user_id to prevent tampering
    task_create.user_id = current_user.id

    task = TaskService.create_task(session, task_create)
    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task for a user."""
    # Ensure user can only access their own tasks
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    task = TaskService.get_task_by_id(session, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific task for a user."""
    # Ensure user can only update their own tasks
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update these tasks"
        )

    updated_task = TaskService.update_task(session, task_id, current_user.id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific task for a user."""
    # Ensure user can only delete their own tasks
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete these tasks"
        )

    success = TaskService.delete_task(session, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Toggle the completion status of a specific task for a user."""
    # Ensure user can only update their own tasks
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update these tasks"
        )

    task = TaskService.toggle_task_completion(session, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task