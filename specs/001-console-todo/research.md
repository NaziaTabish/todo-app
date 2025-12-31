# Research: Phase I - In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Date**: 2025-12-31
**Purpose**: Document technology choices and architecture decisions for Phase I console application

## Overview

This research documents all technology and architectural decisions for Phase I of the Hackathon Todo App Evolution. Phase I builds a foundation in-memory console application using Python 3.13+ with no external dependencies, following the constitution's fixed technology stack per phase.

## Technology Choices

### Language: Python 3.13+

**Decision**: Python 3.13+ as specified in constitution Phase I stack

**Rationale**:
- Constitution explicitly mandates Python 3.13+ for Phase I
- Python provides clean syntax ideal for rapid prototyping in hackathon timeframe
- Strong type hints support (Python 3.13+) enables better code quality and IDE assistance
- Standard library suffices for in-memory CRUD operations (no external dependencies)
- Cross-platform compatibility (Linux, macOS, Windows via WSL2) supports team diversity

**Alternatives Considered**:
- Python 3.11 or 3.12: Rejected - constitution mandates 3.13+ for current hackathon
- Alternative languages (Node.js, Go): Not evaluated - constitution fixes technology stack per phase

### Package Manager: uv

**Decision**: uv for Python dependency and project management

**Rationale**:
- Constitution Phase I stack explicitly requires uv
- Faster than pip for dependency resolution and installation
- Modern tooling with better lock file management
- Supports pyproject.toml (Python packaging standard)
- Faster dependency resolution critical for hackathon timeline

**Alternatives Considered**:
- pip with requirements.txt: Rejected - uv is mandated by constitution
- pip-tools: Not evaluated - constitution fixes uv as standard

### Storage: In-Memory (Python Data Structures)

**Decision**: In-memory storage using Python data structures (list, dict), no persistence

**Rationale**:
- Constitution Phase I explicitly requires in-memory storage ("no database")
- Eliminates persistence layer complexity for Phase I foundation
- Faster to implement (no database setup, migrations, I/O operations)
- Meets spec's Out of Scope requirements (persistent storage is Phase II)
- Supports all CRUD operations with simple data structures

**Data Structure Choice**:
- `Task` as Python dataclass with id, title, description, completed status
- `TodoManager` maintains list of Task objects
- Sequential integer IDs (starting from 1) for simplicity

**Alternatives Considered**:
- File-based storage (JSON, CSV): Rejected - constitution Phase I excludes persistent storage
- SQLite database: Rejected - Phase II introduces Neon PostgreSQL
- Redis in-memory cache: Overkill for single-user CLI, no persistence needed

### Testing Framework: pytest

**Decision**: pytest for unit and integration testing

**Rationale**:
- Constitution mentions "pytest" as testing framework example
- Industry standard for Python testing
- Simple, readable test syntax
- Built-in fixtures and parametrization
- Excellent IDE integration
- Supports both unit and integration tests

**Alternatives Considered**:
- unittest (standard library): Functional but less readable syntax, fewer features
- nose2: Deprecated project, not recommended

### Project Structure: Single Project (Monolithic)

**Decision**: Single project with layered architecture (models, services, cli)

**Rationale**:
- Phase I is console application - no frontend/backend separation needed
- Constitution monorepo principle supports single project structure
- Layered architecture maintains clean separation of concerns
- Simplifies hackathon logistics (single repository, atomic commits)
- Clear migration path to Phase II (backend/ structure will emerge)

**Layer Responsibilities**:
- `models/`: Data entities (Task)
- `services/`: Business logic (task CRUD operations, TodoManager)
- `cli/`: User interface (menu display, input handling)
- `lib/`: Utilities and exceptions

**Alternatives Considered**:
- Flat structure (all files in root): Violates clean code principles, poor organization
- Over-engineered microservices: Unnecessary for single-process CLI application

### Interactive Menu: Python Standard Library

**Decision**: Python standard library for CLI (input, print, sys, argparse)

**Rationale**:
- No external dependencies required (constitution Phase I encourages standard library)
- Simple interactive menu using while loops and input()
- argparse optional for command-line arguments if needed
- Reduces surface area for external library issues

**Menu Design**:
- Display numbered options (1-6 for Add/View/Complete/Delete/Update/Exit)
- Continuous loop until user selects Exit
- Clear prompts and error messages
- Input validation for numeric choices

**Alternatives Considered**:
- Click/Typer: External libraries, overkill for Phase I scope
- Rich/curses: Visual enhancement not needed for Phase I, adds complexity

### Clean Code Standards: PEP 8, Docstrings, Type Hints

**Decision**: Strict adherence to PEP 8, comprehensive docstrings, type hints throughout

**Rationale**:
- Constitution Clean Code Standards principle explicitly requires:
  - Descriptive names (no abbreviations)
  - Docstrings for public functions/classes
  - Proper module structure
  - Consistent formatting
- Type hints (Python 3.13+) improve code quality and IDE support
- PEP 8 is Python style guide (automatic with linters)
- Critical for hackathon pace and team collaboration

**Implementation Approach**:
- Use dataclasses for entities (automatic __init__, __repr__)
- Type hints on all function signatures
- Docstrings on all public methods (Google or NumPy style)
- Black formatter for consistent code style
- mypy for static type checking (optional but recommended)

**Alternatives Considered**:
- Relaxed coding standards: Violates constitution principle, risks quality under time pressure

## Architecture Decisions

### State Management Pattern

**Decision**: Centralized TodoManager class holding application state

**Rationale**:
- Single source of truth for task list
- Encapsulates CRUD operations (create, read, update, delete, toggle)
- Clear separation from UI layer (cli/)
- Enables easier testing (mock TodoManager for CLI tests)
- Supports clean refactoring for Phase II (service layer persists)

**TodoManager Responsibilities**:
- Maintain list of Task objects
- Generate sequential IDs
- Validate inputs (non-empty titles, valid IDs)
- Provide CRUD methods with proper error handling
- Raise custom exceptions for invalid operations

**Alternatives Considered**:
- Global state (module-level list): Harder to test, violates encapsulation
- Multiple manager classes: Over-engineering for Phase I scope

### Error Handling Strategy

**Decision**: Custom exceptions with clear messages, no crashes from invalid input

**Rationale**:
- Spec FR-008 requires "handle invalid task IDs gracefully with clear error messages"
- Spec SC-004 requires "handle invalid inputs...without crashing"
- Custom exceptions provide structure and catchability
- Graceful degradation improves user experience

**Exception Hierarchy**:
- `TodoException` (base)
  - `TaskNotFoundException` (invalid ID for update/delete/complete)
  - `InvalidTitleException` (empty or whitespace-only title)
  - `DuplicateIDException` (shouldn't occur with sequential IDs but defensive)

**Alternatives Considered**:
- Return None/Error codes: Less Pythonic, harder to distinguish error types
- SystemExit on errors: Violates graceful degradation requirement

### Input Validation Strategy

**Decision**: Validate at service layer, propagate to UI with clear messages

**Rationale**:
- Single validation point (TodoManager) ensures consistency
- Clear error messages for users (FR-008, FR-009)
- Prevents invalid state from entering system

**Validation Rules**:
- Title: Non-empty, stripped of leading/trailing whitespace
- Task ID: Positive integer within existing ID range
- Description: Optional (can be None or empty string)

**Alternatives Considered**:
- UI-only validation: Risk of bypass, business logic unaware of invalid state

## Dependencies and Constraints

### No External Dependencies (Standard Library Only)

**Rationale**:
- Constitution Phase I mentions no external dependencies beyond standard library
- Reduces installation complexity
- Faster setup for hackathon demo
- Eliminates dependency conflicts
- Meets "no manual coding" constraint (simpler to generate via Claude Code)

**Standard Library Modules Used**:
- `dataclasses`: Task entity definition
- `typing`: Type hints (Optional, List, etc.)
- `sys`: Exit codes
- Optional: `argparse` (if command-line arguments added)

### Constraints Checklist

- ✅ In-memory only (data lost on exit)
- ✅ No database (Phase II introduces Neon PostgreSQL)
- ✅ No web interface (Phase II introduces Next.js/FastAPI)
- ✅ No authentication (Phase II introduces Better Auth)
- ✅ Single user (no multi-user support)
- ✅ No persistent storage (files, database, etc.)
- ✅ Standard library only (no external dependencies)
- ✅ WSL 2 compatible (all paths and commands work in WSL2)

## Summary

All technology and architecture decisions align with:
1. **Constitution Phase I stack**: Python 3.13+, uv, in-memory storage
2. **Constitution principles**: Spec-driven development, clean code standards, monorepo
3. **Feature requirements**: All functional requirements addressed (FR-001 through FR-010)
4. **Success criteria**: Technology supports measurable outcomes (30s add task, 5s mark complete)
5. **Out of scope**: No persistence, no database, no web/auth (appropriate for Phase I)

No NEEDS CLARIFICATION items - all decisions grounded in constitution and spec.

## Next Steps (Phase 1)

1. Generate data-model.md with Task entity definition
2. Generate API contracts (N/A for Phase I CLI)
3. Generate quickstart.md with setup and usage instructions
4. Run agent context update script to document Phase I choices
5. Re-check Constitution Check post-design
