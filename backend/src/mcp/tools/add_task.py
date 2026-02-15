"""Add task MCP tool for creating new tasks via chat.

Phase III: AI-Powered Todo Chatbot - User Story 1
"""

from typing import Dict, Any, Optional
from sqlmodel import Session
from ...database.database import engine
from ...models.task import Task, TaskCreate
from ...services.task_service import TaskService


async def add_task_handler(
    title: str,
    description: Optional[str] = None,
    user_id: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """Create a new task for the user.

    Args:
        title: The task title
        description: Optional task description
        user_id: The authenticated user's ID

    Returns:
        Dict with created task information or error message
    """
    if not user_id:
        return {"error": "User authentication required"}

    if not title or not title.strip():
        return {"error": "Task title is required"}

    # Clean up the title
    title = title.strip()

    # Create task via service
    with Session(engine) as session:
        task_service = TaskService(session)

        task_data = TaskCreate(
            title=title,
            description=description.strip() if description else None,
            priority=3  # Default to Low priority
        )

        try:
            task = task_service.create_task(user_id=user_id, task=task_data)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority
                },
                "message": f"Created task: {task.title}"
            }
        except Exception as e:
            return {
                "error": f"Failed to create task: {str(e)}"
            }


# Tool metadata for registration
ADD_TASK_TOOL = {
    "name": "add_task",
    "description": "Create a new task for the user. Use this when the user wants to add, create, or remember something.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The task title - what the user wants to do"
            },
            "description": {
                "type": "string",
                "description": "Optional additional details about the task"
            }
        },
        "required": ["title"]
    },
    "handler": add_task_handler
}
