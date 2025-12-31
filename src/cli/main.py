"""Main entry point for todo application.

This module provides application entry point and main loop
for in-memory console todo application.
"""

from services.todo_manager import TaskList
from cli.menu import Menu


def main() -> None:
    """Main application entry point.

    Initializes TodoManager and Menu, then runs continuous
    menu loop until user selects Exit option.
    """
    # Initialize service layer
    todo_manager = TaskList()

    # Initialize menu interface
    menu = Menu(todo_manager)

    # Main application loop
    while True:
        # Display menu
        menu.display()

        # Get user choice
        choice = menu.get_user_choice()

        # Execute selected action
        if choice in menu.MENU_OPTIONS:
            action = menu.MENU_OPTIONS[choice][1]
            action()
        else:
            print(f"❌ Error: Invalid choice '{choice}'. Please enter 1-6.")
            print()


if __name__ == "__main__":
    main()
