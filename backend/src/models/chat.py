"""Chat models for AI-powered todo chatbot.

Phase III: AI-Powered Todo Chatbot
Defines ChatMessage, ChatSession, and API request/response schemas.
"""

from datetime import datetime, timedelta
from typing import Optional, Literal, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Represents a single chat message in a conversation."""

    id: UUID = Field(default_factory=uuid4)
    session_id: str
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[List[dict]] = None
    metadata: Optional[dict] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class ChatSession(BaseModel):
    """Represents a chat session for a user."""

    id: str  # user_id as string
    user_id: object  # UUID from auth system
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    ttl_minutes: int = 30

    @property
    def is_expired(self) -> bool:
        """Check if session has expired due to inactivity."""
        return datetime.utcnow() - self.last_activity > timedelta(minutes=self.ttl_minutes)

    def add_message(self, role: Literal["user", "assistant"], content: str, **kwargs) -> ChatMessage:
        """Add a message and update last activity."""
        message = ChatMessage(
            session_id=self.id,
            role=role,
            content=content,
            **kwargs
        )
        self.messages.append(message)
        self.last_activity = datetime.utcnow()
        return message


# API Request/Response Models

class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=2000, description="User's message")


class TaskInfo(BaseModel):
    """Task information included in chat responses."""

    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    priority: Optional[int] = None


class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    message: str = Field(..., description="Assistant's response")
    tool_used: Optional[str] = Field(None, description="MCP tool that was invoked")
    task_affected: Optional[TaskInfo] = Field(None, description="Task that was created/modified/deleted")


class ChatHistoryResponse(BaseModel):
    """Response containing chat history."""

    messages: List[ChatMessage]
    session_created: datetime
    last_activity: datetime
