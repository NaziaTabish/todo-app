"""Menu interface for todo application.

This module provides interactive menu display and input handling
for all user operations (add, view, complete, update, delete, exit).
"""

import sys
import os
from typing import Optional

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.todo_manager import TaskList
from src.lib.exceptions import TaskNotFoundException, InvalidTitleException


def display_menu() -> None:
    """Display main menu to user.

    Shows all available options with numbered choices.
    """
    _print_header("=== Todo Manager ===")
    print()
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark as Complete")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Exit")
    print()


def get_user_choice() -> str:
    """Prompt user for menu choice.

    Returns:
        User's menu selection (string format)
    """
    return input("Enter your choice (1-6): ").strip()


def get_task_title() -> str:
    """Prompt user for task title.

    Returns:
        Stripped task title from user input
    """
    return input("Task title: ").strip()


def get_task_description() -> Optional[str]:
    """Prompt user for optional task description.

    Returns:
        Stripped description or None if user skips
    """
    desc = input("Task description (optional, press Enter to skip): ").strip()
    return desc if desc else None


def get_task_id(prompt: str = "Task ID: ") -> int:
    """Prompt user for task ID.

    Args:
        prompt: Custom prompt text (default: "Task ID: ")

    Returns:
        Validated task ID as integer
    """
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❌ Error: Please enter a valid number")


def handle_add_task(todo_manager: TaskList) -> None:
    """Handle Add Task menu option."""
    print()
    _print_header("Add Task")
    print("─────────────────────")

    # Get user input
    title = get_task_title()
    description = get_task_description()

    try:
        # Create task via service
        task = todo_manager.add_task(title, description)
        print(f"✓ Task created: ID {task.id} - {task.title}")
    except InvalidTitleException as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error: Failed to create task - {e}")

    print()


def handle_view_tasks(todo_manager: TaskList) -> None:
    """Handle View Tasks menu option."""
    print()
    _print_header("View Tasks")
    print("─────────────────────")

    tasks = todo_manager.list_all_tasks()

    if todo_manager.is_empty():
        print("Task list is empty. Add tasks first.")
        print()
        return

    print(f"Task List ({todo_manager.task_count()} tasks):")
    print()

    for task in tasks:
        status_icon = "✓" if task.completed else "✗"
        status_text = "Complete" if task.completed else "Incomplete"
        desc = task.description or ""

        print(f"ID {task.id}: {task.title}")
        print(f"     Status: {status_icon} {status_text}")
        if desc:
            print(f"     Desc: {desc}")
        print()


def handle_complete_task(todo_manager: TaskList) -> None:
    """Handle Mark as Complete menu option."""
    print()
    _print_header("Mark as Complete")
    print("─────────────────────")

    task_id = get_task_id()

    try:
        task = todo_manager.toggle_completion(task_id)
        status = "complete" if task.completed else "incomplete"
        print(f"✓ Task {task_id} marked as {status}")
    except TaskNotFoundException as e:
        print(f"❌ Error: {e}")

    print()


def handle_update_task(todo_manager: TaskList) -> None:
    """Handle Update Task menu option."""
    print()
    _print_header("Update Task")
    print("─────────────────────")

    task_id = get_task_id()

    try:
        # Show current task details
        task = todo_manager.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)

        print(f"Current task:")
        print(f"  Title: {task.title}")
        print(f"  Description: {task.description or '(none)'}")
        print()

        # Get new values
        print("Enter new values (press Enter to keep current):")
        new_title = input(f"New title: ").strip()
        new_desc = input(f"New description: ").strip() or None

        # Update task
        if not new_title:  # User wants to keep current title
            new_title = None

        updated_task = todo_manager.update_task(
            task_id,
            title=new_title,
            description=new_desc
        )
        print(f"✓ Task {task_id} updated")
    except TaskNotFoundException as e:
        print(f"❌ Error: {e}")
    except InvalidTitleException as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error: Failed to update task - {e}")

    print()


def handle_delete_task(todo_manager: TaskList) -> None:
    """Handle Delete Task menu option."""
    print()
    _print_header("Delete Task")
    print("─────────────────────")

    task_id = get_task_id()

    try:
        todo_manager.delete_task(task_id)
        print(f"✓ Task {task_id} deleted")
    except TaskNotFoundException as e:
        print(f"❌ Error: {e}")

    print()


def handle_exit() -> None:
    """Handle Exit menu option."""
    print()
    print("─────────────────────")
    print("Goodbye!")
    print()


def _print_header(title: str) -> None:
    """Print formatted header with separator line.

    Args:
        title: Header text to display
    """
    separator = "=" * len(title)
    print(separator)
    print(title)
    print(separator)
    print()
