"""Chat API endpoints for AI-powered todo chatbot.

Phase III: AI-Powered Todo Chatbot
Provides endpoints for chat messages and history management.
Includes rate limiting to prevent abuse.
"""

from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from ...models.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from ...models.user import User
from ...services.chat_service import chat_service
from ..deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


# Simple in-memory rate limiter
class RateLimiter:
    """Simple in-memory rate limiter for chat endpoint."""
    
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in the window
            window_seconds: Time window in seconds
        """
        self._requests: dict = defaultdict(list)
        self._max_requests = max_requests
        self._window = timedelta(seconds=window_seconds)
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed to make a request.
        
        Args:
            user_id: The user's ID
            
        Returns:
            True if allowed, False if rate limited
        """
        now = datetime.utcnow()
        cutoff = now - self._window
        
        # Clean old requests
        self._requests[user_id] = [
            ts for ts in self._requests[user_id] if ts > cutoff
        ]
        
        # Check if under limit
        if len(self._requests[user_id]) >= self._max_requests:
            return False
        
        # Record this request
        self._requests[user_id].append(now)
        return True
    
    def get_wait_time(self, user_id: int) -> int:
        """Get seconds until user can make another request.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Seconds to wait (0 if not rate limited)
        """
        if not self._requests[user_id]:
            return 0
        
        oldest = min(self._requests[user_id])
        wait = (oldest + self._window) - datetime.utcnow()
        return max(0, int(wait.total_seconds()))


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=20, window_seconds=60)


@router.post("", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """Send a chat message and receive agent response.

    The AI agent will interpret the message and execute the appropriate
    task operation (add, list, complete, delete, or update).

    Rate limited to 20 messages per minute per user.

    Args:
        request: ChatRequest containing the user's message
        current_user: Authenticated user from JWT token

    Returns:
        ChatResponse with agent's reply and any affected tasks
        
    Raises:
        HTTPException 429 if rate limited
    """
    # Check rate limit
    if not rate_limiter.is_allowed(current_user.id):
        wait_time = rate_limiter.get_wait_time(current_user.id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"You're sending messages too quickly! Please wait {wait_time} seconds and try again. 🐢"
        )
    
    try:
        response = await chat_service.process_message(
            user_id=current_user.id,
            message=request.message
        )
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="I'm having trouble right now. Please try again in a moment."
        )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    current_user: User = Depends(get_current_user)
) -> ChatHistoryResponse:
    """Get the current session's chat history.

    Returns the list of messages in the current chat session.
    Sessions expire after 30 minutes of inactivity.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        ChatHistoryResponse with message list and session info

    Raises:
        HTTPException 404 if no active session exists
    """
    history = chat_service.get_history(current_user.id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active chat session found. Start a conversation first!"
        )
    return history


@router.delete("/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user)
) -> dict:
    """Clear the current session's chat history.

    Removes all messages from the current chat session.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        Confirmation message
    """
    cleared = chat_service.clear_history(current_user.id)
    if cleared:
        return {"message": "Chat history cleared"}
    return {"message": "No chat history to clear"}

