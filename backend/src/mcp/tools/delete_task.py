"""Delete task MCP tool for removing tasks via chat.

Phase III: AI-Powered Todo Chatbot - User Story 4
"""

from typing import Dict, Any, Optional, List
from sqlmodel import Session
from ...database.database import engine
from ...services.task_service import TaskService
from .complete_task import fuzzy_match_tasks


async def delete_task_handler(
    task_identifier: str,
    user_id: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """Delete a task.

    Args:
        task_identifier: Task title or partial match
        user_id: The authenticated user's ID

    Returns:
        Dict with deleted task info or error message
    """
    if not user_id:
        return {"error": "User authentication required"}

    if not task_identifier or not task_identifier.strip():
        return {"error": "Please specify which task to delete"}

    with Session(engine) as session:
        task_service = TaskService(session)

        try:
            # Get all tasks for user
            all_tasks = task_service.get_tasks(user_id=user_id)

            # Find matching tasks
            matches = fuzzy_match_tasks(all_tasks, task_identifier)

            if not matches:
                return {
                    "error": f"I couldn't find a task matching '{task_identifier}'.",
                    "message": f"I couldn't find a task matching '{task_identifier}'. Try 'show my tasks' to see your list."
                }

            if len(matches) > 1:
                # Multiple matches - ask for clarification
                match_titles = [f"'{t.title}'" for t in matches[:5]]
                return {
                    "error": "Multiple tasks match",
                    "matches": [{"id": t.id, "title": t.title} for t in matches],
                    "message": f"I found multiple tasks matching '{task_identifier}': {', '.join(match_titles)}. Which one did you want to delete?"
                }

            # Single match - delete it
            task = matches[0]
            task_title = task.title

            task_service.delete_task(user_id=user_id, task_id=task.id)

            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task_title,
                    "deleted": True
                },
                "message": f"Got it! I've removed '{task_title}' from your list."
            }

        except Exception as e:
            return {
                "error": f"Failed to delete task: {str(e)}"
            }


# Tool metadata for registration
DELETE_TASK_TOOL = {
    "name": "delete_task",
    "description": "Delete a task from the user's list. Use this when the user wants to delete, remove, or cancel a task.",
    "parameters": {
        "type": "object",
        "properties": {
            "task_identifier": {
                "type": "string",
                "description": "The task title or part of it to identify which task to delete"
            }
        },
        "required": ["task_identifier"]
    },
    "handler": delete_task_handler
}
