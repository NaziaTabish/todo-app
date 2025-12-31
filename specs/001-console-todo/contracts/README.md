# API Contracts: Phase I - In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Date**: 2025-12-31

## Overview

Phase I is a command-line interface (CLI) application with in-memory storage. No API contracts are required because:

1. **No External API**: Application is monolithic CLI process
2. **No HTTP Interface**: No REST/GraphQL endpoints (Phase II introduces FastAPI)
3. **No Service Boundaries**: Single process, no microservices or inter-service communication
4. **In-Memory Only**: No database schema or external integrations

## Why No Contracts

### API Contracts Apply When:
- Multiple services communicate via network protocols
- External APIs require request/response schemas
- Database schemas need formal definition
- Frontend/backend integration requires interface contracts

### Phase I Context:
- Single Python process runs CLI application
- User interacts via `input()` and `print()` functions
- All business logic resides in one codebase
- No network communication or external dependencies

## User Interface Protocol (Informal)

While not a formal API contract, the CLI interface follows a simple protocol:

### Menu Display Format
```
=== Todo Manager ===

1. Add Task
2. View Tasks
3. Mark as Complete
4. Update Task
5. Delete Task
6. Exit

Enter your choice (1-6):
```

### User Interaction Flow
1. Application displays menu options (numbered 1-6)
2. User enters numeric choice
3. Application prompts for required inputs based on choice
4. User provides input (text for title/description, integer for task ID)
5. Application displays result (success message or error)
6. Return to step 1 (loop until Exit selected)

### Input Prompts (Informal)
```
Add Task
─────────────────────
Task title: <user input>
Task description (optional, press Enter to skip): <user input>
✓ Task created: ID 1 - Buy groceries

Mark as Complete
─────────────────────
Task ID: <user input>
✓ Task 1 marked as complete
```

### Error Messages (Informal)
```
❌ Error: Task title cannot be empty
❌ Error: Task ID 99 not found
❌ Error: Task list is empty. Add tasks first.
```

## Phase II Evolution

When Phase II introduces the web application, API contracts will be needed:

- **OpenAPI 3.0 specification** for FastAPI endpoints
- **Request/response schemas** for task CRUD operations
- **Authentication contract** for Better Auth with JWT
- **Frontend/backend integration** via REST API

Contracts for Phase II will be generated in `/specs/002-web-todo/contracts/`

## Summary

Phase I requires no formal API contracts due to:
- Single-process CLI architecture
- In-memory storage (no database schema)
- No network communication or external dependencies
- Direct user interaction via standard I/O

All interface specifications are captured in:
- Data model: `data-model.md` (Task and TaskList entities)
- User scenarios: `spec.md` (Given/When/Then acceptance scenarios)
- UI behavior: Informal protocols above (menu format, prompts, errors)
