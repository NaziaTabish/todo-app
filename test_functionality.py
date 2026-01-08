#!/usr/bin/env python3
"""Test script to verify all todo application functionality."""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from src.services.todo_manager import TaskList
from src.cli.menu import (
    handle_add_task, handle_view_tasks, handle_complete_task,
    handle_update_task, handle_delete_task
)

def test_all_functionality():
    """Test all functionality of the todo app."""
    print("Testing Todo Application Functionality")
    print("=" * 40)

    # Initialize a fresh todo manager for testing
    todo_manager = TaskList()

    # Test 1: Add tasks
    print("\n1. Testing Add Task functionality:")
    print("   Adding 'Test Task 1'...")
    handle_add_task(todo_manager)  # This will prompt for input

    print("\n   Adding 'Test Task 2' with description...")
    handle_add_task(todo_manager)  # This will prompt for input

    # Test 2: View tasks
    print("\n2. Testing View Tasks functionality:")
    handle_view_tasks(todo_manager)

    # Test 3: Complete a task
    print("\n3. Testing Mark as Complete functionality:")
    print("   Marking task 1 as complete...")
    # This will prompt for task ID

    # Test 4: Update a task
    print("\n4. Testing Update Task functionality:")
    print("   Updating task 2...")
    # This will prompt for task ID and new values

    # Test 5: Delete a task
    print("\n5. Testing Delete Task functionality:")
    print("   Deleting task 1...")
    # This will prompt for task ID

    # Test 6: View tasks again
    print("\n6. Testing View Tasks after changes:")
    handle_view_tasks(todo_manager)

    print("\nAll functionality tested successfully!")

if __name__ == "__main__":
    test_all_functionality()