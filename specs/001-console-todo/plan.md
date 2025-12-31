# Implementation Plan: Phase I - In-Memory Python Console Todo App

**Branch**: `001-console-todo` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a command-line todo application with in-memory storage that provides basic CRUD functionality: create, read, update, delete, and toggle task completion status. The application uses Python 3.13+ with an interactive menu interface, adhering to clean code principles (PEP 8, docstrings, type hints). All code must be generated via Claude Code following the spec-driven development workflow. This is Phase I of a 5-phase evolution (Console→Web→Chatbot→Local K8s→Cloud).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only for Phase I in-memory implementation)
**Storage**: In-memory (Python data structures: list/dict, no persistence)
**Testing**: pytest for unit tests
**Target Platform**: Command-line interface (CLI) on Linux/macOS/WSL2
**Project Type**: Single project (monolithic CLI application)
**Performance Goals**: Instant response times for all CRUD operations (<50ms), no observable latency for user interactions
**Constraints**: In-memory only (data lost on exit), no external dependencies (standard library), must pass PEP 8 linting
**Scale/Scope**: Single-user application, typical usage 10-50 tasks per session, no multi-user support

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gates

- ✅ **Spec-Driven Development**: All code MUST be generated via Claude Code from this plan and tasks.md - NO manual coding
- ✅ **Phase-Based Evolution**: This is Phase I (Console), before Phase II (Web) - correct sequential progression
- ✅ **Monorepo Organization**: Single project structure, no frontend/backend separation needed for Phase I
- ✅ **Clean Code Standards**: Plan includes PEP 8, docstrings, type hints - will enforce during implementation
- ✅ **WSL 2 for Windows**: All commands assume WSL 2 environment for Windows users
- ✅ **Security & Secrets**: No secrets or credentials needed for Phase I (in-memory, no external services)
- ✅ **AI-First Development**: Not applicable to Phase I (AI features start Phase III) - constitution compliant
- ✅ **Cloud-Native Architecture**: Not applicable to Phase I (Docker/K8s start Phase IV) - constitution compliant

### Post-Design Gates (to be re-checked after Phase 1)

- ✅ All design artifacts (research.md, data-model.md, contracts/) trace back to spec requirements
- ✅ Technology choices match constitution Phase I stack exactly (Python 3.13+, uv, in-memory storage)
- [ ] No manual coding deviations from spec-driven workflow (verified during implementation)

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py             # Task entity with dataclass/model definition
├── services/
│   ├── task_service.py     # Task CRUD business logic
│   └── todo_manager.py    # Main application state and orchestration
├── cli/
│   ├── menu.py            # Interactive menu display and input handling
│   └── main.py            # Application entry point
└── lib/
    └── exceptions.py      # Custom exception definitions

tests/
├── contract/                 # Not applicable for Phase I (no API contracts)
├── integration/
│   └── test_todo_manager.py    # End-to-end workflow tests
└── unit/
    ├── test_task_model.py
    ├── test_task_service.py
    └── test_menu.py

pyproject.toml               # Project metadata and dependencies (uv)
README.md                     # Setup instructions, usage guide
CLAUDE.md                     # Claude Code development instructions
```

**Structure Decision**: Single project structure with clear separation: models (data), services (business logic), cli (interface), lib (utilities). Tests organized by type (unit, integration). This follows constitution's monorepo principle and clean code standards. Phase I doesn't require frontend/backend separation - that begins in Phase II.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations. All gates pass with clear justification:
- Phase I correctly positioned before Phase II-V in evolution sequence
- Technology stack matches constitution Phase I requirements exactly
- Clean code standards (PEP 8, docstrings, type hints) will be enforced
- WSL 2 environment assumed for all development commands
- No external services/secrets needed for Phase I (appropriate for in-memory app)
