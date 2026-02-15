# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/` (FastAPI + OpenAI Agents SDK + MCP SDK)
- **Frontend**: `frontend/src/` (Next.js + OpenAI ChatKit)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and create project structure for chatbot feature

- [X] T001 Add OpenAI and MCP dependencies to backend/requirements.txt
- [X] T002 Add OpenAI ChatKit dependency to frontend/package.json
- [X] T003 [P] Add OPENAI_API_KEY to backend/.env.example
- [X] T004 [P] Create backend/src/mcp/ directory structure with __init__.py
- [X] T005 [P] Create backend/src/agents/ directory structure with __init__.py
- [X] T006 [P] Create frontend/src/components/Chat/ directory structure
- [X] T007 [P] Create frontend/src/context/ChatContext.tsx placeholder

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core chat infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Create ChatMessage model in backend/src/models/chat.py per data-model.md
- [X] T009 Create ChatSession model in backend/src/models/chat.py per data-model.md
- [X] T010 Create ChatSessionStore for in-memory session management in backend/src/services/chat_session_store.py
- [X] T011 Create ChatRequest and ChatResponse schemas in backend/src/models/chat.py
- [X] T012 [P] Create MCP server setup in backend/src/mcp/server.py with tool registry
- [X] T013 [P] Create todo_agent.py with OpenAI Agents SDK configuration in backend/src/agents/todo_agent.py
- [X] T014 Create ChatService skeleton in backend/src/services/chat_service.py (orchestrates agent + tools)
- [X] T015 Create chat API endpoint POST /api/v1/chat in backend/src/api/v1/chat.py
- [X] T016 Create chat history endpoint GET /api/v1/chat/history in backend/src/api/v1/chat.py
- [X] T017 Create clear history endpoint DELETE /api/v1/chat/history in backend/src/api/v1/chat.py
- [X] T018 Register chat router in backend/src/main.py
- [X] T019 [P] Create chat.ts API client service in frontend/src/services/chat.ts
- [X] T020 [P] Create ChatContext provider in frontend/src/context/ChatContext.tsx
- [X] T021 Create ChatMessage component in frontend/src/components/Chat/ChatMessage.tsx
- [X] T022 Create ChatInput component in frontend/src/components/Chat/ChatInput.tsx
- [X] T023 Create ChatWidget component in frontend/src/components/Chat/ChatWidget.tsx
- [X] T024 Integrate ChatWidget into dashboard in frontend/src/pages/dashboard.tsx

**Checkpoint**: Foundation ready - chat UI visible, API endpoint working, agent configured

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by typing "add [task]", "create [task]", or "remember [task]"

**Independent Test**: Type "add buy milk" in chat and verify task appears in task list

### Implementation for User Story 1

- [X] T025 [P] [US1] Create add_task MCP tool in backend/src/mcp/tools/add_task.py
- [X] T026 [US1] Register add_task tool in backend/src/mcp/server.py
- [X] T027 [US1] Add add_task tool definition to agent in backend/src/agents/todo_agent.py
- [X] T028 [US1] Implement add_task handler that calls TaskService.create_task()
- [X] T029 [US1] Add agent instructions for recognizing "add", "create", "remember" intents
- [X] T030 [US1] Add friendly confirmation response generation for task creation
- [ ] T031 [US1] Test add_task flow end-to-end: chat input → agent → tool → TaskService → DB

**Checkpoint**: User Story 1 complete - can create tasks via natural language

---

## Phase 4: User Story 2 - View Tasks via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can view tasks by typing "show my tasks", "what do I need to do?", or "show completed"

**Independent Test**: Type "show my tasks" and verify formatted task list appears

### Implementation for User Story 2

- [X] T032 [P] [US2] Create list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py
- [X] T033 [US2] Register list_tasks tool in backend/src/mcp/server.py
- [X] T034 [US2] Add list_tasks tool definition to agent in backend/src/agents/todo_agent.py
- [X] T035 [US2] Implement list_tasks handler with filter support (all, pending, completed)
- [X] T036 [US2] Add agent instructions for recognizing "show", "see", "what" intents
- [X] T037 [US2] Format task list output with checkboxes (☐/✓) for readability
- [X] T038 [US2] Handle empty task list with friendly message
- [ ] T039 [US2] Test list_tasks flow end-to-end: chat input → agent → tool → formatted response

**Checkpoint**: User Stories 1 AND 2 complete - can create and view tasks via chat

---

## Phase 5: User Story 3 - Complete Tasks via Chat (Priority: P2)

**Goal**: Users can mark tasks complete by typing "done with [task]", "finished [task]", "complete [task]"

**Independent Test**: Create a task, type "done with [task name]", verify task shows as completed

### Implementation for User Story 3

- [X] T040 [P] [US3] Create complete_task MCP tool in backend/src/mcp/tools/complete_task.py
- [X] T041 [US3] Register complete_task tool in backend/src/mcp/server.py
- [X] T042 [US3] Add complete_task tool definition to agent in backend/src/agents/todo_agent.py
- [X] T043 [US3] Implement fuzzy task matching by title in backend/src/mcp/tools/complete_task.py
- [X] T044 [US3] Implement complete_task handler that finds and toggles task
- [X] T045 [US3] Add agent instructions for recognizing "done", "complete", "finished" intents
- [X] T046 [US3] Handle task not found with helpful error message
- [X] T047 [US3] Handle multiple matches by listing options and asking for clarification
- [ ] T048 [US3] Test complete_task flow end-to-end

**Checkpoint**: User Stories 1, 2, AND 3 complete - can create, view, and complete tasks

---

## Phase 6: User Story 4 - Delete Tasks via Chat (Priority: P2)

**Goal**: Users can delete tasks by typing "delete [task]", "remove [task]", "cancel [task]"

**Independent Test**: Create a task, type "delete [task name]", verify task is removed

### Implementation for User Story 4

- [X] T049 [P] [US4] Create delete_task MCP tool in backend/src/mcp/tools/delete_task.py
- [X] T050 [US4] Register delete_task tool in backend/src/mcp/server.py
- [X] T051 [US4] Add delete_task tool definition to agent in backend/src/agents/todo_agent.py
- [X] T052 [US4] Implement delete_task handler using fuzzy matching
- [X] T053 [US4] Add agent instructions for recognizing "delete", "remove", "cancel" intents
- [X] T054 [US4] Handle task not found with helpful error message
- [ ] T055 [US4] Test delete_task flow end-to-end

**Checkpoint**: User Stories 1-4 complete - full CRUD via chat except update

---

## Phase 7: User Story 5 - Update Tasks via Chat (Priority: P3)

**Goal**: Users can update tasks by typing "change [old] to [new]", "update [task] to [new]"

**Independent Test**: Create a task, type "change [task name] to [new name]", verify title updated

### Implementation for User Story 5

- [X] T056 [P] [US5] Create update_task MCP tool in backend/src/mcp/tools/update_task.py
- [X] T057 [US5] Register update_task tool in backend/src/mcp/server.py
- [X] T058 [US5] Add update_task tool definition to agent in backend/src/agents/todo_agent.py
- [X] T059 [US5] Implement update_task handler with old/new title parsing
- [X] T060 [US5] Add agent instructions for recognizing "change", "update", "modify" intents
- [X] T061 [US5] Handle task not found with helpful error message
- [ ] T062 [US5] Test update_task flow end-to-end

**Checkpoint**: All 5 user stories complete - full natural language task management

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T063 Add rate limiting middleware for chat endpoint in backend/src/api/v1/chat.py
- [ ] T064 [P] Add session cleanup background task for expired sessions
- [X] T065 [P] Improve error handling with actionable suggestions per research.md
- [X] T066 [P] Add loading state and typing indicator to ChatWidget
- [X] T067 [P] Style ChatWidget with glass effect matching existing UI
- [X] T068 [P] Add keyboard shortcuts (Enter to send, Escape to close)
- [X] T069 Update frontend/src/pages/dashboard.tsx to show chat toggle button
- [X] T070 [P] Add help command that lists available chat operations
- [ ] T071 Validate all success criteria from spec.md (SC-001 through SC-006)
- [ ] T072 Run quickstart.md validation to ensure setup instructions work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 and US2 are both P1 priority and should be done first
  - US3 and US4 are P2 priority, can be done after US1/US2
  - US5 is P3 priority, lowest priority
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational - Needs fuzzy matching (benefits from US2)
- **User Story 4 (P2)**: Can start after Foundational - Uses same fuzzy matching as US3
- **User Story 5 (P3)**: Can start after Foundational - Uses same fuzzy matching

### Within Each User Story

- Create tool file first
- Register in MCP server
- Add to agent configuration
- Implement handler logic
- Update agent instructions
- Test end-to-end

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Tool creation tasks (T025, T032, T040, T049, T056) can run in parallel
- US1 and US2 can be developed in parallel (both P1)
- US3 and US4 can be developed in parallel (both P2)
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: Setup Phase

```bash
# Launch all parallel setup tasks together:
Task: "Add OPENAI_API_KEY to backend/.env.example"
Task: "Create backend/src/mcp/ directory structure with __init__.py"
Task: "Create backend/src/agents/ directory structure with __init__.py"
Task: "Create frontend/src/components/Chat/ directory structure"
Task: "Create frontend/src/context/ChatContext.tsx placeholder"
```

## Parallel Example: MCP Tools

```bash
# After Foundational phase, launch all tool creation in parallel:
Task: "Create add_task MCP tool in backend/src/mcp/tools/add_task.py"
Task: "Create list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py"
Task: "Create complete_task MCP tool in backend/src/mcp/tools/complete_task.py"
Task: "Create delete_task MCP tool in backend/src/mcp/tools/delete_task.py"
Task: "Create update_task MCP tool in backend/src/mcp/tools/update_task.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add tasks)
4. Complete Phase 4: User Story 2 (View tasks)
5. **STOP and VALIDATE**: Demo creating and viewing tasks via chat
6. Deploy/demo MVP if ready

### Incremental Delivery

1. Setup + Foundational → Chat UI visible, agent configured
2. Add US1 + US2 → MVP: Can add and view tasks (Demo!)
3. Add US3 → Can mark tasks complete (Demo!)
4. Add US4 → Can delete tasks (Demo!)
5. Add US5 → Can update tasks (Complete!)
6. Polish → Production-ready

### Task Count Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Phase 1: Setup | 7 | 5 |
| Phase 2: Foundational | 17 | 4 |
| Phase 3: US1 (Add) | 7 | 1 |
| Phase 4: US2 (View) | 8 | 1 |
| Phase 5: US3 (Complete) | 9 | 1 |
| Phase 6: US4 (Delete) | 7 | 1 |
| Phase 7: US5 (Update) | 7 | 1 |
| Phase 8: Polish | 10 | 6 |
| **Total** | **72** | **20** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = US1 + US2 (add and view tasks via chat)
