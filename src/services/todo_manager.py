"""TaskList service for todo application.

This module defines the TaskList class which manages a collection
of Task objects and provides CRUD operations (create, read, update, delete).
All tasks are stored in-memory and are lost when application exits.
"""

import sys
import os
from typing import List, Optional

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.task import Task
from src.lib.exceptions import TaskNotFoundException, InvalidTitleException


class TaskList:
    """Manages in-memory collection of tasks.

    This class provides the core business logic for all CRUD operations
    including task creation, retrieval, update, deletion, and completion
    toggling. Tasks are stored in a Python list and maintain
    insertion order (creation time).

    Attributes:
        tasks: List of all Task objects in creation order
        next_id: Counter for generating sequential task IDs

    Invariants:
        - tasks list maintains insertion order
        - next_id is always greater than highest existing task ID
        - No duplicate id values exist in tasks list
    """

    def __init__(self) -> None:
        """Initialize empty task list with ID counter starting at 1."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create and add a new task to the list.

        Args:
            title: Task name (non-empty, whitespace-stripped)
            description: Optional task details (whitespace-stripped if provided)

        Returns:
            The newly created Task with auto-generated ID

        Raises:
            InvalidTitleException: If title is empty or whitespace-only

        Validation:
            - Title must be non-empty after stripping
            - Description is optional, stripped if provided
        """
        # Validate title
        if not title or not title.strip():
            raise InvalidTitleException()

        # Create task with next sequential ID
        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        # Add to list and increment ID counter
        self.tasks.append(task)
        self.next_id += 1

        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its unique identifier.

        Args:
            task_id: Unique task identifier to search for

        Returns:
            Task if found, None if ID doesn't exist

        Performance:
            O(n) linear search through task list
            Acceptable for Phase I scale (10-50 tasks)
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Task:
        """Update task title and/or description.

        Args:
            task_id: Unique identifier of task to update
            title: New task name (optional, None to keep current)
            description: New task details (optional, None to keep current)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundException: If task_id doesn't exist
            InvalidTitleException: If new title is empty

        Validation:
            - Task must exist with given ID
            - New title (if provided) must be non-empty after stripping
            - Description (if provided) is stripped
        """
        # Find task
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)

        # Update title if provided
        if title is not None:
            if not title.strip():
                raise InvalidTitleException()
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description.strip() if description else None

        return task

    def delete_task(self, task_id: int) -> None:
        """Remove a task from the list by ID.

        Args:
            task_id: Unique identifier of task to delete

        Raises:
            TaskNotFoundException: If task_id doesn't exist

        Side Effects:
            - Task is removed from tasks list
            - Task ID is not reused (IDs remain sequential without gaps)
        """
        # Find task
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)

        # Remove from list
        self.tasks.remove(task)

    def toggle_completion(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Unique identifier of task to toggle

        Returns:
            Task with updated completion status

        Raises:
            TaskNotFoundException: If task_id doesn't exist

        State Transition:
            incomplete (completed=False) ↔ complete (completed=True)
        """
        # Find task
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)

        # Toggle completion status
        task.toggle_completion()

        return task

    def list_all_tasks(self) -> List[Task]:
        """Return all tasks in creation order.

        Returns:
            List of all tasks (empty list if no tasks exist)
        """
        return self.tasks.copy()

    def task_count(self) -> int:
        """Return the total number of tasks.

        Returns:
            Count of tasks in the list
        """
        return len(self.tasks)

    def is_empty(self) -> bool:
        """Check if task list is empty.

        Returns:
            True if no tasks exist, False otherwise
        """
        return len(self.tasks) == 0
