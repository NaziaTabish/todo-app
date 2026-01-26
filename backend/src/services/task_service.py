"""Task service for Todo application."""

import logging
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskService:
    """Service class for task-related operations."""

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> Task:
        """Create a new task."""
        # Ensure user_id is UUID
        user_id = task_create.user_id
        if not isinstance(user_id, UUID):
            user_id = UUID(str(user_id))

        logger.info(f"Creating new task for user ID: {user_id}")

        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id,
            due_date=task_create.due_date,
            priority=task_create.priority if task_create.priority is not None else 1
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        logger.info(f"Successfully created task with ID: {db_task.id}")
        return db_task

    @staticmethod
    def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Get a task by ID for a specific user."""
        try:
            t_id = UUID(str(task_id)) if not isinstance(task_id, UUID) else task_id
            u_id = UUID(str(user_id)) if not isinstance(user_id, UUID) else user_id
            statement = select(Task).where(Task.id == t_id, Task.user_id == u_id)
            return session.exec(statement).first()
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str, # Changed type hint to reflect reality and internal conversion
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Task]:
        """Get all tasks for a specific user with optional filtering."""
        try:
            target_user_id = UUID(str(user_id)) if not isinstance(user_id, UUID) else user_id
            statement = select(Task).where(Task.user_id == target_user_id)
        except (ValueError, AttributeError):
            return []

        # Apply status filter if provided
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)

        # Apply pagination
        statement = statement.offset(offset).limit(limit).order_by(Task.created_at.desc())

        return session.exec(statement).all()

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task for a specific user."""
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Update fields if provided
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.completed is not None:
            db_task.completed = task_update.completed
        if task_update.due_date is not None:
            db_task.due_date = task_update.due_date
        if task_update.priority is not None:
            db_task.priority = task_update.priority

        # Update timestamp
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """Delete a task for a specific user."""
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Toggle the completion status of a task."""
        db_task = TaskService.get_task_by_id(session, task_id, user_id)
        if not db_task:
            return None

        # Toggle completion status
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task