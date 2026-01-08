"""Main entry point for todo application.

This module provides application entry point and main loop
for in-memory console todo application.
"""

import sys
import os

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.todo_manager import TaskList
from src.cli.menu import display_menu, get_user_choice, handle_add_task, handle_view_tasks
from src.cli.menu import handle_complete_task, handle_update_task, handle_delete_task, handle_exit


def main() -> None:
    """Main application entry point.

    Initializes TodoManager and runs continuous
    menu loop until user selects Exit option.
    """
    # Initialize service layer
    todo_manager = TaskList()

    # Main application loop
    while True:
        # Display menu
        display_menu()

        # Get user choice
        choice = get_user_choice()

        # Execute selected action based on choice
        if choice == "1":
            handle_add_task(todo_manager)
        elif choice == "2":
            handle_view_tasks(todo_manager)
        elif choice == "3":
            handle_complete_task(todo_manager)
        elif choice == "4":
            handle_update_task(todo_manager)
        elif choice == "5":
            handle_delete_task(todo_manager)
        elif choice == "6":
            handle_exit()
            break  # Exit the application
        else:
            print(f"❌ Error: Invalid choice '{choice}'. Please enter 1-6.")
            print()


if __name__ == "__main__":
    main()
