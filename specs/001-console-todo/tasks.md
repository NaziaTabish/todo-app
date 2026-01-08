---

description: "Task list for Phase I - In-Memory Python Console Todo App implementation"
---

# Tasks: Phase I - In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL for Phase I - only generate them if following spec-driven TDD approach requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown follow plan.md structure exactly

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python 3.13+ project with uv package manager
- [X] T003 [P] Configure linting tools (pycodestyle for PEP 8 compliance)
- [X] T004 [P] Create pyproject.toml with project metadata and dependencies
- [X] T005 [P] Create .gitignore file (exclude __pycache__, .venv/, *.pyc)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create lib/exceptions.py with custom exception classes (TodoException, TaskNotFoundException, InvalidTitleException)
- [X] T007 [P] Create src/models/task.py with Task dataclass (id, title, description, completed)
- [X] T008 [P] Create src/services/todo_manager.py with TaskList class and CRUD operations
- [X] T009 Create src/cli/menu.py with menu display and input handling functions
- [X] T010 Create src/cli/main.py with application entry point and main loop
- [X] T011 [P] Add docstrings to all public functions and classes
- [X] T012 [P] Add type hints to all function signatures

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new todo items with title and description, then view all tasks in a list showing their completion status.

**Independent Test**: Launch application, add 3-5 tasks with titles/descriptions, verify they appear in task list with correct details and status indicators.

### Implementation for User Story 1

- [X] T013 [US1] Implement task creation with title and description in src/services/todo_manager.py (add_task method)
- [X] T014 [US1] Implement task list display in src/services/todo_manager.py (list_all_tasks method)
- [X] T015 [US1] Integrate add task menu option in src/cli/menu.py (option 1)
- [X] T016 [US1] Integrate view tasks menu option in src/cli/menu.py (option 2)
- [X] T017 [US1] Add input validation for task title in src/cli/menu.py (non-empty check)
- [X] T018 [US1] Add error handling for invalid input in src/cli/menu.py (clear error messages)
- [X] T019 [US1] Add empty list message handling in src/services/todo_manager.py (FR-010)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add and view tasks.

---

## Phase 4: User Story 2 - Complete Tasks (Priority: P2)

**Goal**: Users can mark existing tasks as complete or incomplete, toggling their status to track progress and visually distinguish finished work.

**Independent Test**: Add tasks, mark them complete/incomplete, verify status indicators change correctly in task list.

### Implementation for User Story 2

- [X] T020 [US2] Implement task completion toggle in src/services/todo_manager.py (toggle_completion method)
- [X] T021 [US2] Integrate mark complete menu option in src/cli/menu.py (option 3)
- [X] T022 [US2] Add task ID validation for toggle operation in src/services/todo_manager.py (raise TaskNotFoundException)
- [X] T023 [US2] Add status indicator display in task list output (✓ complete, ✗ incomplete)
- [X] T024 [US2] Add error handling for invalid task IDs in toggle operation (FR-008)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can create, view, and complete tasks.

---

## Phase 5: User Story 3 - Update and Delete Tasks (Priority: P3)

**Goal**: Users can modify existing task details (title and/or description) and remove tasks they no longer need, providing full CRUD capability and task lifecycle management.

**Independent Test**: Add a task, modify its title/description and verify changes, then delete it and confirm removal.

### Implementation for User Story 3

- [X] T025 [US3] Implement task update in src/services/todo_manager.py (update_task method)
- [X] T026 [US3] Implement task deletion in src/services/todo_manager.py (delete_task method)
- [X] T027 [US3] Integrate update task menu option in src/cli/menu.py (option 4)
- [X] T028 [US3] Integrate delete task menu option in src/cli/menu.py (option 5)
- [X] T029 [US3] Add partial update support in src/cli/menu.py (keep current title/description if empty input)
- [X] T030 [US3] Add error handling for update/delete with invalid IDs in src/cli/menu.py
- [X] T031 [US3] Add input validation for updated title in src/services/todo_manager.py (FR-009)

**Checkpoint**: All user stories should now be independently functional. Full CRUD capability available (create, read, update, delete, toggle complete).

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T032 [P] Add exit menu option in src/cli/menu.py (option 6 with graceful termination)
- [X] T033 [P] Add menu loop in src/cli/main.py (continuous display until exit selected)
- [X] T034 [P] Improve error message formatting across all operations (consistent prefix/suffix)
- [X] T035 [P] Add task list header with task count (e.g., "Task List (3 tasks)")
- [X] T036 [P] Add whitespace stripping to all text inputs (title, description)
- [X] T037 [P] Add clean code compliance check (PEP 8 style formatting)
- [X] T038 Verify all success criteria (SC-001 through SC-005) with manual testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (US1 → US2 → US3)
  - Each story builds on previous story's patterns but remains independently testable
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 task list but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1/US2 patterns but independently testable

### Within Each User Story

- Models before services
- Services before menu options
- Input validation before error handling
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] (T001-T005) can run in parallel
- All Foundational tasks marked [P] (T007-T012) can run in parallel within Phase 2
- Polish tasks marked [P] (T032-T036) can run in parallel within Phase 6
- User stories should be implemented sequentially in priority order (US1 → US2 → US3) for clarity

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks in parallel:
Task: "Create lib/exceptions.py with custom exception classes"
Task: "Create src/models/task.py with Task dataclass"
Task: "Create src/services/todo_manager.py with TaskList class"
Task: "Create src/cli/menu.py with menu display and input handling"
Task: "Create src/cli/main.py with application entry point"
Task: "Add docstrings to all public functions and classes"
Task: "Add type hints to all function signatures"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T019)
4. **STOP and VALIDATE**: Test User Story 1 independently (create and view tasks)
5. Test SC-001: Add first task and see in list within 30 seconds
6. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add Polish (Phase 6) → Final demo preparation
6. Each story adds value without breaking previous stories

### Sequential User Story Strategy

Given single developer scenario:
1. Team completes Setup + Foundational together
2. Implement User Story 1 in priority order (create, view)
3. Implement User Story 2 (toggle completion, status indicators)
4. Implement User Story 3 (update, delete tasks)
5. Complete Polish phase (exit, consistency, improvements)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All code MUST follow clean code standards (PEP 8, docstrings, type hints)
- Use standard library only (no external dependencies)
- Constitution requires spec-driven development - NO manual coding
- All code MUST be generated via Claude Code from these tasks
- Verify tests fail before implementing if following TDD approach
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Validate all success criteria (SC-001 through SC-005) before final submission
- Prepare 90-second demo video showing all features working
