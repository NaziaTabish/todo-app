# Data Model: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-08
**Status**: Complete

## Entity Overview

This feature introduces chat-specific entities while reusing existing Task and User entities from Phase II.

## New Entities

### ChatMessage

Represents a single message in the conversation (user input or bot response).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Unique message identifier |
| session_id | string | Yes | Reference to chat session |
| role | enum | Yes | "user" or "assistant" |
| content | string | Yes | Message text content |
| timestamp | datetime | Yes | When message was sent |
| tool_calls | json | No | MCP tool invocations (for assistant messages) |
| metadata | json | No | Additional context (e.g., intent detected) |

**Validation Rules**:
- `content` must be non-empty, max 2000 characters
- `role` must be one of: "user", "assistant"
- `timestamp` defaults to current UTC time

**State Transitions**: N/A (messages are immutable once created)

### ChatSession

Represents a conversation session tied to an authenticated user.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Session identifier (user_id based) |
| user_id | integer | Yes | Reference to User entity |
| messages | list | Yes | List of ChatMessage objects |
| created_at | datetime | Yes | Session start time |
| last_activity | datetime | Yes | Last message timestamp |
| ttl_minutes | integer | Yes | Time-to-live (default: 30) |

**Validation Rules**:
- `user_id` must reference valid authenticated user
- `messages` ordered by timestamp ascending
- Session expires after `ttl_minutes` of inactivity

**State Transitions**:
- `active` → `expired` (after TTL with no activity)

## Existing Entities (from Phase II)

### Task (reused)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Yes | Primary key |
| title | string | Yes | Task title |
| description | string | No | Task description |
| completed | boolean | Yes | Completion status |
| priority | integer | Yes | 1=High, 2=Medium, 3=Low |
| user_id | integer | Yes | Owner reference |
| created_at | datetime | Yes | Creation timestamp |
| updated_at | datetime | Yes | Last update timestamp |
| due_date | datetime | No | Optional due date |

### User (reused)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Yes | Primary key |
| email | string | Yes | Unique email |
| username | string | Yes | Display name |
| hashed_password | string | Yes | Bcrypt hash |
| first_name | string | No | User's first name |
| last_name | string | No | User's last name |
| created_at | datetime | Yes | Registration timestamp |

## Entity Relationships

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│     User     │───1:N─│  ChatSession │───1:N─│ ChatMessage  │
└──────────────┘       └──────────────┘       └──────────────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│     Task     │
└──────────────┘
```

- **User → ChatSession**: One user can have multiple sessions (but only one active at a time)
- **ChatSession → ChatMessage**: One session contains many messages
- **User → Task**: One user owns many tasks (existing from Phase II)

## Python Models

### ChatMessage Model

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID, uuid4

class ChatMessage(BaseModel):
    """Represents a single chat message."""

    id: UUID = Field(default_factory=uuid4)
    session_id: str
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[list[dict]] = None
    metadata: Optional[dict] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
```

### ChatSession Model

```python
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List

class ChatSession(BaseModel):
    """Represents a chat session for a user."""

    id: str  # user_id as string
    user_id: int
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    ttl_minutes: int = 30

    @property
    def is_expired(self) -> bool:
        """Check if session has expired due to inactivity."""
        return datetime.utcnow() - self.last_activity > timedelta(minutes=self.ttl_minutes)

    def add_message(self, role: str, content: str, **kwargs) -> ChatMessage:
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
```

## API Request/Response Models

### ChatRequest

```python
class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
```

### ChatResponse

```python
class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    message: str = Field(..., description="Assistant's response")
    tool_used: Optional[str] = Field(None, description="MCP tool that was invoked")
    task_affected: Optional[dict] = Field(None, description="Task that was created/modified/deleted")
```

### ChatHistoryResponse

```python
class ChatHistoryResponse(BaseModel):
    """Response containing chat history."""

    messages: List[ChatMessage]
    session_created: datetime
    last_activity: datetime
```

## Storage Strategy

| Entity | Storage | Persistence |
|--------|---------|-------------|
| ChatMessage | In-memory (dict) | Session-only |
| ChatSession | In-memory (dict) | Session-only (30min TTL) |
| Task | PostgreSQL | Permanent |
| User | PostgreSQL | Permanent |

**Rationale**: Per spec, chat history is session-based only. In-memory storage avoids database migration and complexity. Tasks persist permanently via existing Phase II infrastructure.

## Index/Query Patterns

### ChatSession Queries
- `get_session(user_id)` - O(1) dictionary lookup
- `cleanup_expired()` - O(n) scan, run periodically

### Task Queries (existing)
- `find_by_title_fuzzy(user_id, query)` - SQL LIKE for partial matching
- `list_by_status(user_id, filter)` - SQL WHERE clause

## Data Migration

**No migration required** - ChatMessage and ChatSession are in-memory only. Existing Task and User tables unchanged.
