"""Complete task MCP tool for marking tasks as done via chat.

Phase III: AI-Powered Todo Chatbot - User Story 3
"""

from typing import Dict, Any, Optional, List
from sqlmodel import Session
from ...database.database import engine
from ...services.task_service import TaskService


def fuzzy_match_tasks(tasks: List, query: str) -> List:
    """Find tasks that match the query (case-insensitive partial match).

    Args:
        tasks: List of task objects
        query: Search query

    Returns:
        List of matching tasks
    """
    query_lower = query.lower().strip()
    matches = []

    for task in tasks:
        title_lower = task.title.lower()
        # Exact match
        if title_lower == query_lower:
            return [task]  # Exact match, return immediately
        # Partial match
        if query_lower in title_lower or title_lower in query_lower:
            matches.append(task)

    return matches


async def complete_task_handler(
    task_identifier: str,
    user_id: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """Mark a task as complete.

    Args:
        task_identifier: Task title or partial match
        user_id: The authenticated user's ID

    Returns:
        Dict with completed task info or error message
    """
    if not user_id:
        return {"error": "User authentication required"}

    if not task_identifier or not task_identifier.strip():
        return {"error": "Please specify which task to complete"}

    with Session(engine) as session:
        task_service = TaskService(session)

        try:
            # Get all tasks for user
            all_tasks = task_service.get_tasks(user_id=user_id)
            pending_tasks = [t for t in all_tasks if not t.completed]

            # Find matching tasks
            matches = fuzzy_match_tasks(pending_tasks, task_identifier)

            if not matches:
                # Try matching against all tasks (including completed)
                all_matches = fuzzy_match_tasks(all_tasks, task_identifier)
                if all_matches and all(t.completed for t in all_matches):
                    return {
                        "error": f"Task '{task_identifier}' is already completed!",
                        "message": f"The task '{all_matches[0].title}' is already marked as done."
                    }
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
                    "message": f"I found multiple tasks matching '{task_identifier}': {', '.join(match_titles)}. Which one did you mean?"
                }

            # Single match - complete it
            task = matches[0]
            updated_task = task_service.toggle_task_completion(
                user_id=user_id,
                task_id=task.id
            )

            return {
                "success": True,
                "task": {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "completed": updated_task.completed
                },
                "message": f"Done! '{updated_task.title}' is now complete."
            }

        except Exception as e:
            return {
                "error": f"Failed to complete task: {str(e)}"
            }


# Tool metadata for registration
COMPLETE_TASK_TOOL = {
    "name": "complete_task",
    "description": "Mark a task as complete. Use this when the user says they're done, finished, or completed something.",
    "parameters": {
        "type": "object",
        "properties": {
            "task_identifier": {
                "type": "string",
                "description": "The task title or part of it to identify which task to complete"
            }
        },
        "required": ["task_identifier"]
    },
    "handler": complete_task_handler
}
