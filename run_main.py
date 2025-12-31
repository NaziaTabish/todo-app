"""Direct entry point for todo application.

Run with: python run_main.py
"""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Import the modules directly from the src directory
from src.services.todo_manager import TaskList
from src.cli.menu import display_menu, get_user_choice
from src.cli.menu import handle_add_task, handle_view_tasks, handle_complete_task
from src.cli.menu import handle_update_task, handle_delete_task, handle_exit


def main() -> None:
    """Main application entry point."""
    todo_manager = TaskList()

    while True:
        display_menu()
        choice = get_user_choice()

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
