"""Update task MCP tool for modifying tasks via chat.

Phase III: AI-Powered Todo Chatbot - User Story 5
"""

from typing import Dict, Any, Optional
from sqlmodel import Session
from ...database.database import engine
from ...models.task import TaskUpdate
from ...services.task_service import TaskService
from .complete_task import fuzzy_match_tasks


async def update_task_handler(
    task_identifier: str,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None,
    user_id: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """Update a task's title or description.

    Args:
        task_identifier: Current task title or partial match
        new_title: New title for the task
        new_description: New description for the task
        user_id: The authenticated user's ID

    Returns:
        Dict with updated task info or error message
    """
    if not user_id:
        return {"error": "User authentication required"}

    if not task_identifier or not task_identifier.strip():
        return {"error": "Please specify which task to update"}

    if not new_title and not new_description:
        return {"error": "Please provide a new title or description"}

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
                    "message": f"I found multiple tasks matching '{task_identifier}': {', '.join(match_titles)}. Which one did you want to update?"
                }

            # Single match - update it
            task = matches[0]
            old_title = task.title

            # Build update data
            update_data = TaskUpdate()
            if new_title:
                update_data.title = new_title.strip()
            if new_description:
                update_data.description = new_description.strip()

            updated_task = task_service.update_task(
                user_id=user_id,
                task_id=task.id,
                task=update_data
            )

            change_desc = []
            if new_title:
                change_desc.append(f"title to '{new_title}'")
            if new_description:
                change_desc.append("description")

            return {
                "success": True,
                "task": {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "completed": updated_task.completed
                },
                "message": f"Updated! Changed {' and '.join(change_desc)} for '{old_title}'."
            }

        except Exception as e:
            return {
                "error": f"Failed to update task: {str(e)}"
            }


# Tool metadata for registration
UPDATE_TASK_TOOL = {
    "name": "update_task",
    "description": "Update a task's title or description. Use this when the user wants to change, update, modify, or rename a task.",
    "parameters": {
        "type": "object",
        "properties": {
            "task_identifier": {
                "type": "string",
                "description": "The current task title or part of it to identify which task to update"
            },
            "new_title": {
                "type": "string",
                "description": "The new title for the task"
            },
            "new_description": {
                "type": "string",
                "description": "The new description for the task"
            }
        },
        "required": ["task_identifier"]
    },
    "handler": update_task_handler
}
