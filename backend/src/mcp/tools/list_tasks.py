"""List tasks MCP tool for viewing tasks via chat.

Phase III: AI-Powered Todo Chatbot - User Story 2
"""

from typing import Dict, Any, Optional, Literal
from sqlmodel import Session
from ...database.database import engine
from ...services.task_service import TaskService


async def list_tasks_handler(
    filter: Optional[Literal["all", "pending", "completed"]] = "all",
    user_id: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """List tasks for the user with optional filtering.

    Args:
        filter: Filter by status - "all", "pending", or "completed"
        user_id: The authenticated user's ID

    Returns:
        Dict with task list or error message
    """
    if not user_id:
        return {"error": "User authentication required"}

    with Session(engine) as session:
        task_service = TaskService(session)

        try:
            # Get all tasks for user
            all_tasks = task_service.get_tasks(user_id=user_id)

            # Apply filter
            if filter == "pending":
                tasks = [t for t in all_tasks if not t.completed]
            elif filter == "completed":
                tasks = [t for t in all_tasks if t.completed]
            else:
                tasks = all_tasks

            # Format tasks for display
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority
                })

            # Generate formatted message
            if not task_list:
                if filter == "pending":
                    message = "You don't have any pending tasks. Great job!"
                elif filter == "completed":
                    message = "You haven't completed any tasks yet."
                else:
                    message = "You don't have any tasks yet. Try adding one!"
            else:
                lines = []
                for i, task in enumerate(task_list, 1):
                    checkbox = "✓" if task["completed"] else "☐"
                    lines.append(f"{i}. {checkbox} {task['title']}")
                message = "Here are your tasks:\n" + "\n".join(lines)

            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list),
                "filter": filter,
                "message": message
            }

        except Exception as e:
            return {
                "error": f"Failed to list tasks: {str(e)}"
            }


# Tool metadata for registration
LIST_TASKS_TOOL = {
    "name": "list_tasks",
    "description": "List the user's tasks. Use this when the user wants to see, show, view, or check their tasks.",
    "parameters": {
        "type": "object",
        "properties": {
            "filter": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "description": "Filter tasks by status. Use 'pending' for incomplete tasks, 'completed' for done tasks, or 'all' for everything."
            }
        }
    },
    "handler": list_tasks_handler
}
