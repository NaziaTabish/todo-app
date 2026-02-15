"""
MCP Tools API - Direct database operations for the AI agent
These functions are called by the OpenAI Agents SDK function tools
"""

from typing import Optional, List, Any
from pydantic import BaseModel
from sqlmodel import Session, select
from ..database.database import engine
from ..models.task import Task
import uuid


class TaskCreateRequest(BaseModel):
    """Request model for creating a task."""
    title: str
    description: Optional[str] = None
    user_id: Any  # UUID from auth system
    priority: Optional[str] = None  # 'HIGH', 'MEDIUM', 'LOW'
    due_date: Optional[str] = None
    tags: Optional[List[str]] = None
    recurrence_rule: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[List[str]] = None


class TaskFilterRequest(BaseModel):
    """Request model for filtering tasks."""
    user_id: Any  # UUID from auth system
    status: str = "all"  # 'all', 'pending', 'completed'


class TaskResponse(BaseModel):
    """Response model for a task."""
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    priority: int
    user_id: str

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Response model for task list."""
    tasks: List[TaskResponse]
    count: int


def _priority_to_int(priority: Optional[str]) -> int:
    """Convert priority string to integer."""
    if priority == "HIGH":
        return 1
    elif priority == "MEDIUM":
        return 2
    else:
        return 3  # LOW or default


def _task_to_response(task: Task) -> TaskResponse:
    """Convert a Task ORM object to TaskResponse with string IDs."""
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        user_id=str(task.user_id)
    )


def add_task(request: TaskCreateRequest) -> TaskResponse:
    """Create a new task."""
    with Session(engine) as session:
        task = Task(
            title=request.title,
            description=request.description,
            user_id=request.user_id,
            priority=_priority_to_int(request.priority),
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return _task_to_response(task)


def list_tasks(request: TaskFilterRequest) -> TaskListResponse:
    """List tasks with optional filtering."""
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == request.user_id)

        if request.status == "pending":
            statement = statement.where(Task.completed == False)
        elif request.status == "completed":
            statement = statement.where(Task.completed == True)

        tasks = session.exec(statement).all()
        task_responses = [_task_to_response(t) for t in tasks]

        return TaskListResponse(tasks=task_responses, count=len(task_responses))


def complete_task(user_id: Any, task_id: Any, completed: bool = True) -> TaskResponse:
    """Mark a task as completed or pending."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise ValueError(f"Task {task_id} not found")

        task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return _task_to_response(task)


def delete_task(user_id: Any, task_id: Any) -> dict:
    """Delete a task."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {"status": "error", "message": f"Task {task_id} not found"}

        session.delete(task)
        session.commit()
        return {"status": "success", "message": f"Task {task_id} deleted"}


def update_task(user_id: Any, task_id: Any, request: TaskUpdateRequest) -> TaskResponse:
    """Update a task."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise ValueError(f"Task {task_id} not found")

        if request.title is not None:
            task.title = request.title
        if request.description is not None:
            task.description = request.description
        if request.completed is not None:
            task.completed = request.completed
        if request.priority is not None:
            task.priority = _priority_to_int(request.priority)

        session.add(task)
        session.commit()
        session.refresh(task)
        return _task_to_response(task)
