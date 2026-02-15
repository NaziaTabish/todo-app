# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

## Summary

Add a conversational chat interface to the existing Todo application that allows users to manage tasks through natural language. The chatbot will interpret user intent (add, list, complete, delete, update) and execute corresponding task operations using MCP tools backed by OpenAI Agents SDK. The chat UI will be built with OpenAI ChatKit and integrated into the existing Next.js frontend.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/Next.js 16+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI Agents SDK, MCP SDK (Official), SQLModel
- Frontend: Next.js 16+, OpenAI ChatKit, Tailwind CSS
**Storage**: Neon PostgreSQL (existing from Phase II) + session-based chat state
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (desktop/mobile browsers)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <3 second response time for chat messages, 90% intent recognition accuracy
**Constraints**: Stateless chat endpoint, session-based message history, English only
**Scale/Scope**: Single-user sessions, existing task database, 5 MCP tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | This plan derives from spec.md with full traceability |
| II. Phase-Based Evolution | ✅ PASS | Phase III follows Phase II; building on existing web app |
| III. Monorepo Organization | ✅ PASS | Adding to existing backend/ and frontend/ structure |
| IV. Clean Code Standards | ✅ PASS | Will follow naming, docstrings, module structure |
| V. WSL 2 for Windows | ✅ PASS | Development in WSL 2 environment |
| VI. Security & Secrets | ✅ PASS | OpenAI API key in .env, JWT auth reused |
| VII. AI-First Development | ✅ PASS | Using OpenAI Agents SDK + MCP SDK + ChatKit as specified |
| VIII. Cloud-Native Architecture | N/A | Phase IV+ requirement, not applicable to Phase III |

**Technology Stack Compliance (Phase III)**:
- ✅ Chat UI: OpenAI ChatKit
- ✅ AI Backend: OpenAI Agents SDK
- ✅ Tool Integration: Official MCP SDK
- ✅ API Endpoint: Stateless chat endpoint
- ✅ Architecture: Conversational interface over existing backend

**Constitution Gate**: PASSED - All applicable principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output - technology research
├── data-model.md        # Phase 1 output - entity definitions
├── quickstart.md        # Phase 1 output - setup guide
├── contracts/           # Phase 1 output - API contracts
│   └── chat-api.yaml    # OpenAPI spec for chat endpoint
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py          # Existing - reuse
│   │   ├── user.py          # Existing - reuse
│   │   └── chat.py          # NEW - ChatMessage, ChatSession models
│   ├── services/
│   │   ├── task_service.py  # Existing - reuse
│   │   ├── user_service.py  # Existing - reuse
│   │   └── chat_service.py  # NEW - chat orchestration
│   ├── api/
│   │   ├── auth.py          # Existing - reuse
│   │   ├── deps.py          # Existing - reuse (auth dependencies)
│   │   └── v1/
│   │       ├── tasks.py     # Existing - reuse
│   │       └── chat.py      # NEW - chat endpoint
│   ├── mcp/                  # NEW - MCP tools directory
│   │   ├── __init__.py
│   │   ├── server.py        # MCP server setup
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── complete_task.py
│   │       ├── delete_task.py
│   │       └── update_task.py
│   └── agents/               # NEW - OpenAI Agents SDK
│       ├── __init__.py
│       └── todo_agent.py    # Agent configuration
└── tests/
    ├── unit/
    │   └── test_chat_service.py
    └── integration/
        └── test_chat_endpoint.py

frontend/
├── src/
│   ├── components/
│   │   ├── Layout/          # Existing
│   │   ├── TaskItem.tsx     # Existing
│   │   ├── TaskList.tsx     # Existing
│   │   └── Chat/            # NEW - Chat components
│   │       ├── ChatWidget.tsx
│   │       ├── ChatMessage.tsx
│   │       └── ChatInput.tsx
│   ├── pages/
│   │   ├── index.tsx        # Existing
│   │   ├── dashboard.tsx    # Existing - add chat widget
│   │   └── chat.tsx         # NEW - dedicated chat page (optional)
│   ├── services/
│   │   ├── auth.ts          # Existing
│   │   ├── tasks.ts         # Existing
│   │   └── chat.ts          # NEW - chat API client
│   └── context/
│       ├── UserContext.tsx  # Existing
│       └── ChatContext.tsx  # NEW - chat state management
└── tests/
    └── components/
        └── Chat.test.tsx
```

**Structure Decision**: Web application structure (Option 2) - extending existing backend/ and frontend/ directories with new chat-specific modules. MCP tools are organized in a dedicated `backend/src/mcp/` directory for clean separation.

## Complexity Tracking

> No violations - all principles satisfied without exceptions.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  Dashboard  │    │  ChatWidget │    │   OpenAI ChatKit    │  │
│  │   (tasks)   │◄──►│  Component  │◄──►│   (UI framework)    │  │
│  └─────────────┘    └──────┬──────┘    └─────────────────────┘  │
└────────────────────────────┼────────────────────────────────────┘
                             │ HTTP/WebSocket
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Backend (FastAPI)                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ /api/v1/chat│───►│ ChatService │───►│  OpenAI Agents SDK  │  │
│  │  endpoint   │    │             │    │   (orchestration)   │  │
│  └─────────────┘    └──────┬──────┘    └──────────┬──────────┘  │
│                            │                      │              │
│                            ▼                      ▼              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    MCP Server + Tools                        ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       ││
│  │  │ add_task │ │list_tasks│ │complete_ │ │delete_   │ ...   ││
│  │  │          │ │          │ │  task    │ │  task    │       ││
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       ││
│  └───────┼────────────┼────────────┼────────────┼──────────────┘│
│          │            │            │            │                │
│          ▼            ▼            ▼            ▼                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              TaskService (existing from Phase II)            ││
│  └──────────────────────────┬──────────────────────────────────┘│
└─────────────────────────────┼────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Neon PostgreSQL │
                    │   (existing)    │
                    └─────────────────┘
```

## Data Flow

1. **User sends message** → ChatWidget → `/api/v1/chat` endpoint
2. **Endpoint authenticates** → JWT validation via existing auth
3. **ChatService receives message** → passes to OpenAI Agents SDK
4. **Agent interprets intent** → determines which MCP tool to call
5. **MCP tool executes** → calls existing TaskService methods
6. **TaskService persists** → Neon PostgreSQL (existing)
7. **Agent generates response** → friendly confirmation message
8. **Response returns** → ChatWidget displays to user

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chat state persistence | Session-only (in-memory) | Spec defines session-based; simpler; no DB migration |
| Intent recognition | OpenAI Agents SDK | Constitution mandates; handles NLU automatically |
| Tool execution | MCP SDK | Constitution mandates; standardized tool interface |
| Chat UI | OpenAI ChatKit | Constitution mandates; ready-made chat components |
| Auth integration | Reuse existing JWT | Avoid duplication; consistent user experience |
| Task operations | Reuse TaskService | DRY principle; existing tested code |

## Phase 0 Research Topics

1. **OpenAI Agents SDK integration patterns** - How to configure agents with MCP tools
2. **MCP SDK tool definition** - Schema for add_task, list_tasks, etc.
3. **OpenAI ChatKit setup** - Integration with Next.js and styling with Tailwind
4. **Session management** - In-memory vs Redis for chat history
5. **Error handling patterns** - How agents communicate failures gracefully

## Phase 1 Design Outputs

- `research.md` - Consolidated research findings
- `data-model.md` - ChatMessage, ChatSession entities
- `contracts/chat-api.yaml` - OpenAPI spec for chat endpoint
- `quickstart.md` - Developer setup guide

## Next Steps

1. Run `/sp.plan` Phase 0 to generate `research.md`
2. Run `/sp.plan` Phase 1 to generate data model and contracts
3. Run `/sp.tasks` to generate implementation tasks
4. Implement following task order in `tasks.md`
