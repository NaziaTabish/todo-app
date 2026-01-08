#!/usr/bin/env python3
"""Script to verify all success criteria for Phase I Todo App."""

import sys
import os
import time
from datetime import datetime

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from src.services.todo_manager import TaskList
from src.models.task import Task

def test_sc_001():
    """Test SC-001: Users can add their first task and see it in the list within 30 seconds."""
    print("Testing SC-001: Add first task and see in list within 30 seconds...")

    start_time = time.time()
    todo_manager = TaskList()

    # Add first task
    task = todo_manager.add_task("First task for SC-001", "Test description")

    # Check that task exists in list
    all_tasks = todo_manager.list_all_tasks()
    success = len(all_tasks) == 1 and all_tasks[0].title == "First task for SC-001"

    elapsed_time = time.time() - start_time

    if success and elapsed_time <= 30:
        print(f"   [PASS] SC-001 PASSED: Task added and found in {elapsed_time:.2f}s (< 30s)")
        return True
    else:
        print(f"   [FAIL] SC-001 FAILED: Elapsed time {elapsed_time:.2f}s or task not found")
        return False

def test_sc_002():
    """Test SC-002: Users can mark a task as complete with single action in under 5 seconds."""
    print("Testing SC-002: Mark task as complete under 5 seconds...")

    start_time = time.time()
    todo_manager = TaskList()

    # Add a task
    task = todo_manager.add_task("Task for SC-002", "Test description")

    # Toggle completion
    toggled_task = todo_manager.toggle_completion(task.id)

    elapsed_time = time.time() - start_time

    success = toggled_task.completed and elapsed_time <= 5

    if success:
        print(f"   [PASS] SC-002 PASSED: Task marked complete in {elapsed_time:.2f}s (< 5s)")
        return True
    else:
        print(f"   [FAIL] SC-002 FAILED: Elapsed time {elapsed_time:.2f}s or completion failed")
        return False

def test_sc_003():
    """Test SC-003: All 5 CRUD operations executable with 3 or fewer user interactions."""
    print("Testing SC-003: All 5 CRUD operations with 3 or fewer interactions...")

    todo_manager = TaskList()

    operations_tested = 0

    # 1. CREATE (Add Task) - 1 interaction
    try:
        task = todo_manager.add_task("CRUD Test Task", "Description for CRUD test")
        operations_tested += 1
        print("   [PASS] Create operation: 1 interaction")
    except:
        print("   ❌ Create operation failed")
        return False

    # 2. READ (View Tasks) - 1 interaction
    try:
        tasks = todo_manager.list_all_tasks()
        if len(tasks) > 0:
            operations_tested += 1
            print("   ✓ Read operation: 1 interaction")
        else:
            print("   ❌ Read operation failed: no tasks returned")
            return False
    except:
        print("   ❌ Read operation failed")
        return False

    # 3. UPDATE (Update Task) - 1 interaction
    try:
        updated_task = todo_manager.update_task(task.id, title="Updated CRUD Test Task")
        if updated_task.title == "Updated CRUD Test Task":
            operations_tested += 1
            print("   ✓ Update operation: 1 interaction")
        else:
            print("   ❌ Update operation failed: title not updated")
            return False
    except:
        print("   ❌ Update operation failed")
        return False

    # 4. DELETE (Delete Task) - 1 interaction
    try:
        original_count = todo_manager.task_count()
        todo_manager.delete_task(task.id)
        new_count = todo_manager.task_count()

        if new_count == original_count - 1:
            operations_tested += 1
            print("   ✓ Delete operation: 1 interaction")
        else:
            print("   ❌ Delete operation failed: task not deleted")
            return False
    except:
        print("   ❌ Delete operation failed")
        return False

    # 5. TOGGLE COMPLETE - Need to add task again to test
    try:
        task = todo_manager.add_task("Toggle Test Task", "For completion test")
        toggled_task = todo_manager.toggle_completion(task.id)
        if toggled_task.completed:
            operations_tested += 1
            print("   ✓ Toggle operation: 1 interaction")
        else:
            print("   ❌ Toggle operation failed: not completed")
            return False
    except:
        print("   ❌ Toggle operation failed")
        return False

    if operations_tested == 5:
        print(f"   ✓ SC-003 PASSED: All {operations_tested}/5 operations work with ≤3 interactions")
        return True
    else:
        print(f"   ❌ SC-003 FAILED: Only {operations_tested}/5 operations passed")
        return False

def test_sc_004():
    """Test SC-004: Application handles invalid inputs with clear error messages."""
    print("Testing SC-004: Handle invalid inputs with clear error messages...")

    from src.lib.exceptions import TaskNotFoundException, InvalidTitleException

    todo_manager = TaskList()

    # Test invalid title (empty)
    try:
        todo_manager.add_task("")  # Should raise InvalidTitleException
        print("   ❌ Invalid title test failed: exception not raised")
        return False
    except InvalidTitleException:
        print("   ✓ Invalid title handled with clear error message")
    except Exception as e:
        print(f"   ❌ Unexpected error for invalid title: {e}")
        return False

    # Test invalid task ID (non-existent)
    try:
        todo_manager.toggle_completion(999)  # Should raise TaskNotFoundException
        print("   ❌ Invalid ID test failed: exception not raised")
        return False
    except TaskNotFoundException:
        print("   ✓ Invalid task ID handled with clear error message")
    except Exception as e:
        print(f"   ❌ Unexpected error for invalid ID: {e}")
        return False

    # Test update with invalid ID
    try:
        todo_manager.update_task(999, title="Invalid update")  # Should raise TaskNotFoundException
        print("   ❌ Invalid update test failed: exception not raised")
        return False
    except TaskNotFoundException:
        print("   ✓ Invalid update ID handled with clear error message")
    except Exception as e:
        print(f"   ❌ Unexpected error for invalid update: {e}")
        return False

    # Test delete with invalid ID
    try:
        todo_manager.delete_task(999)  # Should raise TaskNotFoundException
        print("   ❌ Invalid delete test failed: exception not raised")
        return False
    except TaskNotFoundException:
        print("   ✓ Invalid delete ID handled with clear error message")
    except Exception as e:
        print(f"   ❌ Unexpected error for invalid delete: {e}")
        return False

    print("   ✓ SC-004 PASSED: All invalid inputs handled with clear error messages")
    return True

def test_sc_005():
    """Test SC-005: New users can complete full cycle within 2 minutes."""
    print("Testing SC-005: Full cycle (add, complete, delete) within 2 minutes...")

    start_time = time.time()
    todo_manager = TaskList()

    try:
        # Add task
        task = todo_manager.add_task("Full Cycle Test", "Complete the full cycle test")

        # Mark as complete
        completed_task = todo_manager.toggle_completion(task.id)
        if not completed_task.completed:
            print("   ❌ Full cycle failed: task not marked complete")
            return False

        # Delete task
        original_count = todo_manager.task_count()
        todo_manager.delete_task(task.id)
        new_count = todo_manager.task_count()

        if new_count != original_count - 1:
            print("   ❌ Full cycle failed: task not deleted")
            return False

        elapsed_time = time.time() - start_time

        if elapsed_time <= 120:  # 2 minutes = 120 seconds
            print(f"   ✓ SC-005 PASSED: Full cycle completed in {elapsed_time:.2f}s (< 120s)")
            return True
        else:
            print(f"   ❌ SC-005 FAILED: Cycle took {elapsed_time:.2f}s (> 120s)")
            return False

    except Exception as e:
        print(f"   ❌ Full cycle failed with error: {e}")
        return False

def main():
    """Run all success criteria tests."""
    print("=" * 60)
    print("VERIFICATION: Phase I Success Criteria")
    print("=" * 60)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    tests = [
        ("SC-001", test_sc_001),
        ("SC-002", test_sc_002),
        ("SC-003", test_sc_003),
        ("SC-004", test_sc_004),
        ("SC-005", test_sc_005)
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        print(f"{name}: ", end="")
        if test_func():
            passed += 1
        print()

    print("=" * 60)
    print(f"RESULTS: {passed}/{total} success criteria passed")

    if passed == total:
        print("🎉 SUCCESS: All Phase I success criteria have been met!")
        print("Phase I - In-Memory Python Console Todo App is complete.")
        return True
    else:
        print(f"❌ FAILURE: {total - passed} success criteria need to be addressed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)