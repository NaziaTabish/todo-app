"""Task entity model for todo application.

This module defines the Task dataclass representing a todo item
with unique identifier, title, optional description, and completion status.
"""

import sys
import os
from dataclasses import dataclass
from typing import Optional

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


@dataclass
class Task:
    """Represents a todo item in the system.

    Attributes:
        id: Unique sequential identifier for the task (starts from 1)
        title: Task name/description (required, non-empty after stripping)
        description: Optional additional task details
        completed: True if task is finished, False otherwise

    State Transition:
        incomplete (completed=False) ←→ complete (completed=True)

    Invariants:
        - id is unique across all tasks in TaskList
        - id is sequential (no gaps in ID sequence)
        - title is non-empty after stripping whitespace
        - completed is boolean (True or False only)
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task data after initialization.

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Strip whitespace from title for consistency
        self.title = self.title.strip()

        # Strip whitespace from description if provided
        if self.description is not None:
            self.description = self.description.strip()

    def toggle_completion(self) -> None:
        """Toggle task completion status.

        Flips the completed flag between True and False.
        """
        self.completed = not self.completed

    def __str__(self) -> str:
        """String representation for display in CLI.

        Returns formatted string showing ID, title, and completion status.
        """
        status_icon = "✓" if self.completed else "✗"
        desc = self.description or ""
        return f"ID {self.id}: {self.title}\n     Status: {status_icon} {'Complete' if self.completed else 'Incomplete'}\n     Desc: {desc}"
