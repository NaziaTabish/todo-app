"""Chat service orchestrating agent and tools.

Phase III: AI-Powered Todo Chatbot
Handles chat message processing and session management.
"""

from typing import Dict, Any, Optional, List
from ..models.chat import ChatResponse, ChatHistoryResponse, TaskInfo
from .chat_session_store import chat_session_store
from ..agents.todo_agent import TaskManagementAgent

# Global agent instance
_agent = TaskManagementAgent()


class ChatService:
    """Service for processing chat messages."""

    async def process_message(
        self,
        user_id: int,
        message: str
    ) -> ChatResponse:
        """Process a user message and return the response.

        Args:
            user_id: The authenticated user's ID
            message: The user's natural language message

        Returns:
            ChatResponse with agent's reply and any affected tasks
        """
        # Get or create session
        session = chat_session_store.get_or_create_session(user_id)

        # Add user message to session
        chat_session_store.add_message(user_id, "user", message)

        # Build conversation history for context
        # Include the current message in the history passed to the agent
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in session.messages
        ]

        # Process with agent
        result = await _agent.chat(
            messages=messages,
            user_id=user_id
        )

        # result format: {"response": str, "action_performed": str, "task_result": Any}

        # Add assistant response to session
        chat_session_store.add_message(
            user_id,
            "assistant",
            result["response"],
            tool_calls=[{"name": result["action_performed"]}] if result.get("action_performed") else None
        )

        # Build response
        task_info = None
        if result.get("task_result"):
            task_data = result["task_result"]
            # Flexible handling of task data format
            if isinstance(task_data, dict):
                # Check for nested task object (from mcp_tools return format)
                if "task" in task_data:
                    task_data = task_data["task"]
                
                task_info = TaskInfo(
                    id=str(task_data.get("id", "")),
                    title=task_data.get("title", ""),
                    description=task_data.get("description"),
                    completed=task_data.get("completed", False),
                    priority=task_data.get("priority")
                )

        return ChatResponse(
            message=result["response"],
            tool_used=result.get("action_performed"),
            task_affected=task_info
        )

    def get_history(self, user_id: int) -> Optional[ChatHistoryResponse]:
        """Get chat history for a user.

        Args:
            user_id: The authenticated user's ID

        Returns:
            ChatHistoryResponse if session exists, None otherwise
        """
        session = chat_session_store.get_session(user_id)
        if not session:
            return None

        return ChatHistoryResponse(
            messages=session.messages,
            session_created=session.created_at,
            last_activity=session.last_activity
        )

    def clear_history(self, user_id: int) -> bool:
        """Clear chat history for a user.

        Args:
            user_id: The authenticated user's ID

        Returns:
            True if history was cleared, False if no session existed
        """
        return chat_session_store.clear_session(user_id)


# Global service instance
chat_service = ChatService()
