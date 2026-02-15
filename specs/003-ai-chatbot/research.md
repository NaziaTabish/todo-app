# Research: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-08
**Status**: Complete

## Research Topics

### 1. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK with function calling for intent recognition and tool execution

**Rationale**:
- OpenAI Agents SDK provides built-in function calling that maps naturally to MCP tools
- Automatic intent recognition from natural language without manual NLU training
- Streaming support for real-time chat responses
- Built-in conversation history management

**Alternatives Considered**:
- LangChain agents: More complex setup, additional dependency
- Custom NLU with regex: Too brittle, poor accuracy for varied input
- Claude API: Different ecosystem, less MCP integration

**Implementation Pattern**:
```python
from openai import OpenAI
from agents import Agent, Runner

# Define tools as functions
tools = [
    {"type": "function", "function": {...}},  # add_task
    {"type": "function", "function": {...}},  # list_tasks
    # etc.
]

# Create agent with tools
agent = Agent(
    name="TodoAssistant",
    instructions="You help users manage their todo tasks...",
    tools=tools
)

# Run with user message
result = Runner.run_sync(agent, messages=[{"role": "user", "content": user_input}])
```

### 2. MCP SDK Tool Definition

**Decision**: Use Official MCP SDK with typed tool schemas

**Rationale**:
- Constitution mandates Official MCP SDK
- Standardized tool interface for agent interaction
- Type safety with Pydantic models
- Built-in validation and error handling

**Tool Schemas**:

```python
# add_task tool
{
    "name": "add_task",
    "description": "Create a new task for the user",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Task title"},
            "description": {"type": "string", "description": "Optional task description"}
        },
        "required": ["title"]
    }
}

# list_tasks tool
{
    "name": "list_tasks",
    "description": "List user's tasks with optional filtering",
    "parameters": {
        "type": "object",
        "properties": {
            "filter": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "description": "Filter tasks by status"
            }
        }
    }
}

# complete_task tool
{
    "name": "complete_task",
    "description": "Mark a task as complete",
    "parameters": {
        "type": "object",
        "properties": {
            "task_identifier": {"type": "string", "description": "Task title or partial match"}
        },
        "required": ["task_identifier"]
    }
}

# delete_task tool
{
    "name": "delete_task",
    "description": "Delete a task",
    "parameters": {
        "type": "object",
        "properties": {
            "task_identifier": {"type": "string", "description": "Task title or partial match"}
        },
        "required": ["task_identifier"]
    }
}

# update_task tool
{
    "name": "update_task",
    "description": "Update a task's title or description",
    "parameters": {
        "type": "object",
        "properties": {
            "task_identifier": {"type": "string", "description": "Current task title or partial match"},
            "new_title": {"type": "string", "description": "New task title"},
            "new_description": {"type": "string", "description": "New task description"}
        },
        "required": ["task_identifier"]
    }
}
```

### 3. OpenAI ChatKit Setup

**Decision**: Use OpenAI ChatKit with custom styling via Tailwind CSS

**Rationale**:
- Constitution mandates ChatKit for Phase III
- Pre-built chat UI components (messages, input, typing indicators)
- React-based, integrates with Next.js
- Customizable via CSS/Tailwind

**Integration Pattern**:
```tsx
import { Chat, useChat } from '@openai/chatkit';

function ChatWidget() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/v1/chat',
    headers: { Authorization: `Bearer ${token}` }
  });

  return (
    <div className="chat-container">
      <Chat
        messages={messages}
        input={input}
        onInputChange={handleInputChange}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
```

**Styling Approach**:
- Use existing Tailwind theme (primary colors, glass effect)
- Chat widget as floating panel on dashboard
- Responsive design for mobile/desktop

### 4. Session Management

**Decision**: In-memory session storage with 30-minute TTL

**Rationale**:
- Spec defines session-based only (no persistence requirement)
- Simpler than Redis; sufficient for single-server deployment
- 30-minute TTL matches SC-005 success criterion
- No database migration required

**Implementation**:
```python
from datetime import datetime, timedelta
from typing import Dict, List

class ChatSessionStore:
    def __init__(self, ttl_minutes: int = 30):
        self.sessions: Dict[str, List[dict]] = {}
        self.last_access: Dict[str, datetime] = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def get_messages(self, user_id: str) -> List[dict]:
        self._cleanup_expired()
        self.last_access[user_id] = datetime.utcnow()
        return self.sessions.get(user_id, [])

    def add_message(self, user_id: str, message: dict):
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        self.sessions[user_id].append(message)
        self.last_access[user_id] = datetime.utcnow()

    def _cleanup_expired(self):
        now = datetime.utcnow()
        expired = [uid for uid, last in self.last_access.items()
                   if now - last > self.ttl]
        for uid in expired:
            del self.sessions[uid]
            del self.last_access[uid]
```

**Alternatives Considered**:
- Redis: Overkill for single server; adds infrastructure
- Database persistence: Out of scope per spec
- Browser localStorage: Can't share across tabs; security concerns

### 5. Error Handling Patterns

**Decision**: Graceful degradation with actionable suggestions

**Rationale**:
- SC-006 requires 100% actionable error messages
- Users should never see technical errors
- Guide users toward correct usage

**Error Categories and Responses**:

| Error Type | User Message |
|------------|--------------|
| Task not found | "I couldn't find a task matching '{query}'. Try 'show my tasks' to see your list." |
| Multiple matches | "I found {n} tasks matching '{query}': {list}. Which one did you mean?" |
| Invalid command | "I'm not sure what you'd like to do. Try: 'add [task]', 'show tasks', 'done [task]', 'delete [task]', or 'update [task] to [new name]'" |
| Auth required | "Please log in to manage your tasks." |
| Service unavailable | "I'm having trouble right now. Please try again in a moment." |
| Rate limited | "You're sending messages too quickly. Please wait a moment." |

**Implementation Pattern**:
```python
class ChatError(Exception):
    def __init__(self, user_message: str, suggestion: str = None):
        self.user_message = user_message
        self.suggestion = suggestion

def handle_chat_error(error: ChatError) -> str:
    response = error.user_message
    if error.suggestion:
        response += f" {error.suggestion}"
    return response
```

## Technology Stack Summary

| Component | Technology | Version |
|-----------|------------|---------|
| AI Orchestration | OpenAI Agents SDK | Latest |
| Tool Interface | Official MCP SDK | Latest |
| Chat UI | OpenAI ChatKit | Latest |
| Backend Framework | FastAPI | 0.100+ |
| Frontend Framework | Next.js | 16+ |
| Styling | Tailwind CSS | 3.x |
| Database | Neon PostgreSQL | (existing) |
| Authentication | JWT via Better Auth | (existing) |

## Dependencies to Add

**Backend (requirements.txt)**:
```
openai>=1.0.0
mcp>=1.0.0
```

**Frontend (package.json)**:
```json
{
  "@openai/chatkit": "^1.0.0"
}
```

## Security Considerations

1. **OpenAI API Key**: Store in `.env` file, never commit
2. **User Isolation**: All MCP tools receive user_id from JWT; enforce in TaskService
3. **Rate Limiting**: Implement per-user rate limits on chat endpoint
4. **Input Validation**: Sanitize user input before passing to agent
5. **Output Filtering**: Ensure agent responses don't leak sensitive data

## Research Complete

All unknowns resolved. Ready for Phase 1 design (data-model.md, contracts/).
