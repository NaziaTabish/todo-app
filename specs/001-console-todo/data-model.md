# Data Model: Phase I - In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Date**: 2025-12-31
**Purpose**: Define data entities and their relationships for in-memory todo management

## Overview

This data model describes the core entities for Phase I console todo application. All entities are stored in-memory using Python data structures. No persistence layer exists (data lost on application exit). This model supports all functional requirements from the specification (FR-001 through FR-010).

## Entities

### Task

Represents a todo item with unique identifier, title, optional description, and completion status.

**Attributes**:

| Attribute | Type | Required | Description | Validation |
|------------|------|-----------|-------------|--------------|
| id | int | Yes | Unique sequential identifier (1, 2, 3, ...) | Auto-generated, positive integer |
| title | str | Yes | Task title/name | Non-empty after stripping whitespace |
| description | str \| None | No | Additional task details | Optional, can be None or empty string |
| completed | bool | Yes | Task completion status | True = complete, False = incomplete |

**Python Implementation (dataclass)**:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """Represents a todo item in the system.

    Attributes:
        id: Unique sequential identifier for the task
        title: Task name/description (required, non-empty)
        description: Optional additional details
        completed: True if task is finished, False otherwise
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
```

**State Transitions**:

```
          create(id, title, description, completed=False)
  ┌─────────────────────────────────────────────────────┐
  │                                                │
  │                                                │
  ▼                                                │
incomplete (completed=False)  ──toggle──►  complete (completed=True)
  ▲                                                │
  │                                                │
  │                              toggle               │
  └──────────────────────────────────────────────────────┘
```

**State Transition Rules**:
- Initial state: `completed=False` (new tasks start incomplete)
- Toggle operation flips state: `completed = not completed`
- No other states exist (binary completion model)

**Invariants**:
- `id` is unique across all tasks in Task List
- `id` is sequential (no gaps in ID sequence)
- `title` is non-empty after stripping whitespace
- `completed` is boolean (True or False only)

### Task List

Represents the collection of all tasks currently being tracked in the application. Stored in-memory as a Python list.

**Attributes**:

| Attribute | Type | Description |
|------------|------|-------------|
| tasks | List[Task] | All tasks in the system (ordered by creation time) |
| next_id | int | Counter for generating next sequential task ID |

**Python Implementation**:

```python
from typing import List, Optional

class TaskList:
    """Manages in-memory collection of tasks.

    Attributes:
        tasks: List of all tasks in creation order
        next_id: Counter for generating sequential IDs
    """

    def __init__(self) -> None:
        """Initialize empty task list with ID counter starting at 1."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create and add a new task to the list.

        Args:
            title: Task name (non-empty)
            description: Optional task details

        Returns:
            The newly created Task with auto-generated ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its unique identifier.

        Args:
            task_id: Unique task identifier to search for

        Returns:
            Task if found, None if ID doesn't exist
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
            ValueError: If new title is empty
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(f"Task ID {task_id} not found")

        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip() if description else None

        return task

    def delete_task(self, task_id: int) -> None:
        """Remove a task from the list by ID.

        Args:
            task_id: Unique identifier of task to delete

        Raises:
            TaskNotFoundException: If task_id doesn't exist
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(f"Task ID {task_id} not found")
        self.tasks.remove(task)

    def toggle_completion(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Unique identifier of task to toggle

        Returns:
            Task with updated completion status

        Raises:
            TaskNotFoundException: If task_id doesn't exist
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(f"Task ID {task_id} not found")
        task.completed = not task.completed
        return task

    def list_all_tasks(self) -> List[Task]:
        """Return all tasks in creation order.

        Returns:
            List of all tasks (empty list if no tasks exist)
        """
        return self.tasks.copy()
```

**Invariants**:
- `tasks` list maintains insertion order (creation time)
- `next_id` is always greater than highest existing task ID
- No duplicate `id` values exist in `tasks` list

## Relationships

```
┌──────────────┐       contains       ┌────────────────┐
│  TaskList    │─────────────────────►│   Task(s)     │
│ (1 instance)  │  0..*           │ (many)        │
└──────────────┘                    └────────────────┘
```

**Relationship Details**:
- One-to-many: TaskList contains 0 or more Task instances
- Task has no relationships to other entities (no subtasks, categories, etc. in Phase I)
- Task maintains no references to TaskList (aggregation, not composition)

## Indexing and Search

**Primary Index**: `id` field on Task
- Sequential integers starting from 1
- Unique across all tasks
- Used for all update/delete/complete operations
- Implemented via linear search (sufficient for Phase I scale)

**Search Operations**:
- `get_task_by_id(id)`: O(n) linear search through task list
- No secondary indexes (title search, status filtering not in scope for Phase I)

**Scale Considerations**:
- Typical usage: 10-50 tasks per session
- Linear search performance: <1ms for 50 tasks
- No optimization needed for Phase I scope

## Data Lifecycle

**Creation**:
1. User provides title (required) and description (optional)
2. TaskList generates sequential ID
3. Task object created with `completed=False`
4. Task appended to TaskList.tasks
5. TaskList.next_id incremented

**Update**:
1. User provides task ID and optional new title/description
2. TaskList.get_task_by_id() locates task
3. Task.title and/or Task.description updated
4. Task object returned with new values

**Completion Toggle**:
1. User provides task ID
2. TaskList.get_task_by_id() locates task
3. Task.completed flipped (True ↔ False)
4. Task object returned with updated status

**Deletion**:
1. User provides task ID
2. TaskList.get_task_by_id() locates task
3. Task removed from TaskList.tasks
4. Task object no longer accessible

**Application Exit**:
- All Task objects in TaskList.tasks are lost
- No persistence layer (in-memory only, per Phase I constraints)

## Data Validation Rules

### Task Title Validation

**Rule**: Title must be non-empty after stripping whitespace

**Implementation**:
```python
if not title or not title.strip():
    raise ValueError("Task title cannot be empty")
```

**Applies To**:
- Task creation (FR-009)
- Task title update

### Task ID Validation

**Rule**: Task ID must exist in TaskList

**Implementation**:
```python
task = self.get_task_by_id(task_id)
if not task:
    raise TaskNotFoundException(f"Task ID {task_id} not found")
```

**Applies To**:
- Task update (FR-004)
- Task deletion (FR-005)
- Task completion toggle (FR-003)

### Task Description Validation

**Rule**: Description is optional (can be None or empty string)

**Implementation**:
```python
description = description.strip() if description else None
```

**Applies To**:
- Task creation
- Task description update

## In-Memory Constraints

**No Persistence**: All data lost on application exit
- TaskList.tasks exists in RAM only
- No file I/O, database, or external storage
- User must re-enter tasks on each launch (Phase I limitation)

**No Concurrency**: Single-threaded application
- No locking or synchronization needed
- Single user sequential operations only
- No multi-user support (Phase I constraint)

**Memory Considerations**:
- Typical task object size: ~200 bytes (title 50 chars, description 100 chars, overhead)
- 50 tasks: ~10 KB RAM (negligible)
- No memory leaks expected (Python GC handles object lifecycle)
