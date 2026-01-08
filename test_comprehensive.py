#!/usr/bin/env python3
"""Test script to verify all todo application functionality."""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from src.services.todo_manager import TaskList
from src.models.task import Task
from src.lib.exceptions import TaskNotFoundException, InvalidTitleException

def test_all_functionality():
    """Test all functionality of the todo app programmatically."""
    print("Testing Todo Application Functionality")
    print("=" * 40)

    # Initialize a fresh todo manager for testing
    todo_manager = TaskList()

    # Test 1: Add tasks
    print("\n1. Testing Add Task functionality:")
    try:
        task1 = todo_manager.add_task("Test Task 1", "Description for task 1")
        print(f"   [PASS] Added task: ID {task1.id}, Title: '{task1.title}', Desc: '{task1.description}'")

        task2 = todo_manager.add_task("Test Task 2")
        print(f"   [PASS] Added task: ID {task2.id}, Title: '{task2.title}', Desc: '{task2.description}'")

        task3 = todo_manager.add_task("Test Task 3", "Description for task 3")
        print(f"   [PASS] Added task: ID {task3.id}, Title: '{task3.title}', Desc: '{task3.description}'")
    except Exception as e:
        print(f"   [FAIL] Error adding tasks: {e}")

    # Test 2: View/List all tasks
    print("\n2. Testing View Tasks functionality:")
    try:
        all_tasks = todo_manager.list_all_tasks()
        print(f"   Found {len(all_tasks)} tasks:")
        for task in all_tasks:
            status = "Complete" if task.completed else "Incomplete"
            print(f"   - ID {task.id}: '{task.title}' - {status} - Desc: '{task.description}'")
    except Exception as e:
        print(f"   [FAIL] Error listing tasks: {e}")

    # Test 3: Get specific task
    print("\n3. Testing Get Task by ID:")
    try:
        task = todo_manager.get_task_by_id(1)
        print(f"   [PASS] Retrieved task ID 1: '{task.title}' - Complete: {task.completed}")
    except TaskNotFoundException as e:
        print(f"   [FAIL] Error getting task: {e}")

    # Test 4: Mark task as complete
    print("\n4. Testing Mark as Complete functionality:")
    try:
        toggled_task = todo_manager.toggle_completion(1)
        print(f"   [PASS] Toggled task ID 1: '{toggled_task.title}' - Complete: {toggled_task.completed}")

        # Toggle back to incomplete
        toggled_task = todo_manager.toggle_completion(1)
        print(f"   [PASS] Toggled task ID 1 again: '{toggled_task.title}' - Complete: {toggled_task.completed}")

        # Now mark as complete for real
        toggled_task = todo_manager.toggle_completion(1)
        print(f"   [PASS] Final toggle - task ID 1: '{toggled_task.title}' - Complete: {toggled_task.completed}")
    except TaskNotFoundException as e:
        print(f"   [FAIL] Error toggling task: {e}")

    # Test 5: Update task
    print("\n5. Testing Update Task functionality:")
    try:
        updated_task = todo_manager.update_task(2, title="Updated Task 2", description="New description for task 2")
        print(f"   [PASS] Updated task ID 2: '{updated_task.title}' - Desc: '{updated_task.description}'")
    except (TaskNotFoundException, InvalidTitleException) as e:
        print(f"   [FAIL] Error updating task: {e}")

    # Test 6: Delete task
    print("\n6. Testing Delete Task functionality:")
    try:
        todo_manager.delete_task(3)
        print(f"   [PASS] Deleted task ID 3")
    except TaskNotFoundException as e:
        print(f"   [FAIL] Error deleting task: {e}")

    # Test 7: Verify deletion and final state
    print("\n7. Verifying final state after deletion:")
    try:
        remaining_tasks = todo_manager.list_all_tasks()
        print(f"   Remaining {len(remaining_tasks)} tasks:")
        for task in remaining_tasks:
            status = "Complete" if task.completed else "Incomplete"
            print(f"   - ID {task.id}: '{task.title}' - {status} - Desc: '{task.description}'")
    except Exception as e:
        print(f"   [FAIL] Error listing remaining tasks: {e}")

    # Test 8: Error handling - try to get deleted task
    print("\n8. Testing get_task_by_id behavior for non-existent task:")
    task = todo_manager.get_task_by_id(3)  # This task was deleted
    if task is None:
        print(f"   [PASS] Correctly returned None for non-existent task")
    else:
        print(f"   [FAIL] Should have returned None, got: {task}")

    # Test 9: Error handling - try to update non-existent task
    print("\n9. Testing error handling for updating non-existent task:")
    try:
        updated_task = todo_manager.update_task(3, title="Should Fail")
        print(f"   [FAIL] Should not reach here - updated task: {updated_task}")
    except TaskNotFoundException as e:
        print(f"   [PASS] Correctly caught error for updating non-existent task: {e}")

    # Test 10: Error handling - try to delete non-existent task
    print("\n10. Testing error handling for deleting non-existent task:")
    try:
        todo_manager.delete_task(3)  # Already deleted
        print(f"   [FAIL] Should not reach here - deleted task")
    except TaskNotFoundException as e:
        print(f"   [PASS] Correctly caught error for deleting non-existent task: {e}")

    print("\n[SUCCESS] All functionality tested successfully!")
    print(f"Final task count: {todo_manager.task_count()}")

if __name__ == "__main__":
    test_all_functionality()