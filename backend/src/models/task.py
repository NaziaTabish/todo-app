"""Task model for Todo application."""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    """Base fields for Task model."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    due_date: Optional[datetime] = Field(default=None)
    priority: int = Field(default=1, ge=1, le=3)  # 1=highest, 3=lowest


class Task(TaskBase, table=True):
    """Task model with database table configuration."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    user_id: uuid.UUID


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Schema for updating task data."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(default=None, ge=1, le=3)