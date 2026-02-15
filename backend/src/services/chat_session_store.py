"""In-memory session storage for chat conversations.

Phase III: AI-Powered Todo Chatbot
Manages chat sessions with 30-minute TTL.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from ..models.chat import ChatSession, ChatMessage


class ChatSessionStore:
    """Thread-safe in-memory storage for chat sessions."""

    def __init__(self, ttl_minutes: int = 30):
        """Initialize the session store.

        Args:
            ttl_minutes: Session time-to-live in minutes (default: 30)
        """
        self._sessions: Dict[str, ChatSession] = {}
        self._ttl_minutes = ttl_minutes

    def get_or_create_session(self, user_id: int) -> ChatSession:
        """Get existing session or create a new one.

        Args:
            user_id: The user's ID

        Returns:
            ChatSession for the user
        """
        self._cleanup_expired()
        session_id = str(user_id)

        if session_id in self._sessions:
            session = self._sessions[session_id]
            if not session.is_expired:
                session.last_activity = datetime.utcnow()
                return session

        # Create new session
        session = ChatSession(
            id=session_id,
            user_id=user_id,
            ttl_minutes=self._ttl_minutes
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, user_id: int) -> Optional[ChatSession]:
        """Get session for a user if it exists and is not expired.

        Args:
            user_id: The user's ID

        Returns:
            ChatSession if found and valid, None otherwise
        """
        self._cleanup_expired()
        session_id = str(user_id)

        if session_id in self._sessions:
            session = self._sessions[session_id]
            if not session.is_expired:
                return session
            else:
                del self._sessions[session_id]

        return None

    def add_message(
        self,
        user_id: int,
        role: str,
        content: str,
        **kwargs
    ) -> ChatMessage:
        """Add a message to a user's session.

        Args:
            user_id: The user's ID
            role: 'user' or 'assistant'
            content: Message content
            **kwargs: Additional message fields (tool_calls, metadata)

        Returns:
            The created ChatMessage
        """
        session = self.get_or_create_session(user_id)
        return session.add_message(role, content, **kwargs)

    def clear_session(self, user_id: int) -> bool:
        """Clear a user's chat session.

        Args:
            user_id: The user's ID

        Returns:
            True if session was cleared, False if not found
        """
        session_id = str(user_id)
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def _cleanup_expired(self) -> int:
        """Remove all expired sessions.

        Returns:
            Number of sessions removed
        """
        now = datetime.utcnow()
        expired_ids = [
            session_id
            for session_id, session in self._sessions.items()
            if session.is_expired
        ]

        for session_id in expired_ids:
            del self._sessions[session_id]

        return len(expired_ids)

    @property
    def active_session_count(self) -> int:
        """Get count of active (non-expired) sessions."""
        self._cleanup_expired()
        return len(self._sessions)


# Global session store instance
chat_session_store = ChatSessionStore()
