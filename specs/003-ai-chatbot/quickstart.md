# Quickstart: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-02-08

## Prerequisites

- Phase II Todo App running (backend + frontend)
- Python 3.13+
- Node.js 18+
- OpenAI API key

## Setup Steps

### 1. Environment Variables

Add to `backend/.env`:
```bash
# Existing variables from Phase II
DATABASE_URL=postgresql://...
JWT_SECRET=...

# NEW for Phase III
OPENAI_API_KEY=sk-your-openai-api-key
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install openai mcp
# or with uv:
uv pip install openai mcp
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install @openai/chatkit
```

### 4. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the Chat

1. Open http://localhost:3000
2. Log in with your account
3. Navigate to Dashboard
4. Find the chat widget in the bottom-right corner

## Quick Test

Try these commands in the chat:

| Command | Expected Result |
|---------|-----------------|
| `add buy milk` | Creates a new task "buy milk" |
| `show my tasks` | Lists all your tasks |
| `done buy milk` | Marks "buy milk" as complete |
| `delete buy milk` | Removes the task |
| `show completed` | Lists completed tasks only |

## Troubleshooting

### "OpenAI API key not configured"

Ensure `OPENAI_API_KEY` is set in `backend/.env` and restart the backend.

### "Unauthorized" errors

Make sure you're logged in. The chat requires authentication.

### "I couldn't find that task"

The task matcher is fuzzy but not perfect. Try using more of the task title.

### Chat not responding

1. Check backend logs for errors
2. Verify OpenAI API key is valid
3. Check rate limits on OpenAI account

## Development Notes

### Adding New Chat Commands

1. Define MCP tool in `backend/src/mcp/tools/`
2. Register in `backend/src/mcp/server.py`
3. Update agent instructions in `backend/src/agents/todo_agent.py`

### Customizing Chat UI

- Styles in `frontend/src/components/Chat/ChatWidget.tsx`
- Uses existing Tailwind theme (primary colors, glass effect)
- ChatKit components are customizable via props

### Testing Chat Functionality

```bash
# Backend unit tests
cd backend
pytest tests/unit/test_chat_service.py -v

# Backend integration tests
pytest tests/integration/test_chat_endpoint.py -v

# Frontend component tests
cd frontend
npm test -- --testPathPattern=Chat
```

## Architecture Reference

See [plan.md](./plan.md) for full architecture diagram and data flow.
