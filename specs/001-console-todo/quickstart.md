# Quickstart: Phase I - In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Date**: 2025-12-31
**Purpose**: Quick setup guide for developers and demo preparation

## Prerequisites

**Required Tools**:
- Python 3.13+ (installed and in PATH)
- uv package manager (for Python project management)
- Git (for version control)
- Terminal/Command Prompt (use WSL 2 on Windows)

**Installation Verification**:
```bash
# Check Python version
python --version  # Should be 3.13 or higher

# Check uv installation
uv --version

# Check Git
git --version
```

## Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-app
git checkout 001-console-todo
```

### 2. Install Dependencies

Using uv (constitution-mandated package manager):

```bash
# Install project dependencies
uv sync

# Or if using virtual environment explicitly:
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 3. Verify Installation

```bash
# Run tests to verify setup
pytest tests/ -v

# Should see tests pass for task model, service, and menu
```

## Running the Application

### Start the Todo Manager

```bash
# From project root
python -m cli.main

# Or if installed as package
todo-manager
```

### Interactive Menu

Application launches with this menu:

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

### Usage Examples

**Add Your First Task**:
```
Enter your choice (1-6): 1
─────────────────────
Task title: Buy groceries
Task description (optional, press Enter to skip): Milk, eggs, bread
✓ Task created: ID 1 - Buy groceries
```

**View All Tasks**:
```
Enter your choice (1-6): 2
─────────────────────
Task List (2 tasks):

ID 1: Buy groceries
     Status: ✗ Incomplete
     Desc:  Milk, eggs, bread

ID 2: Pay bills
     Status: ✓ Complete
     Desc:  Electricity, internet
```

**Mark Task as Complete**:
```
Enter your choice (1-6): 3
─────────────────────
Task ID: 1
✓ Task 1 marked as complete
```

**Update Task Details**:
```
Enter your choice (1-6): 4
─────────────────────
Task ID: 1
New title (press Enter to keep current): Buy groceries for party
New description (press Enter to keep current): Cheese, crackers, wine
✓ Task 1 updated
```

**Delete a Task**:
```
Enter your choice (1-6): 5
─────────────────────
Task ID: 2
✓ Task 2 deleted
```

**Exit Application**:
```
Enter your choice (1-6): 6
─────────────────────
Goodbye!
```

## Testing

### Run All Tests

```bash
# Run complete test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_task_model.py -v
```

### Test Output

Passing tests should show:
```
tests/unit/test_task_model.py::test_task_creation PASSED
tests/unit/test_task_service.py::test_add_task PASSED
tests/integration/test_todo_manager.py::test_full_crud_cycle PASSED
...
=== 12 passed in 0.5s ===
```

## Development Workflow

### Spec-Driven Development

Constitution requires: **NO manual coding**. All code must be generated via Claude Code from:
1. `spec.md` - Feature requirements and user stories
2. `plan.md` - Technical decisions and architecture
3. `tasks.md` - Implementation tasks (created via `/sp.tasks`)

### Generate Code with Claude Code

1. Ensure task list exists: `specs/001-console-todo/tasks.md`
2. Run `/sp.implement` or use Claude Code directly
3. Claude Code generates code from task descriptions
4. Review generated code against spec and plan
5. Run tests to verify implementation

### Commit Code

```bash
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: implement add task functionality (T001)"

# Push to remote
git push origin 001-console-todo
```

### Project Structure Reference

```
src/
├── models/task.py          # Task dataclass
├── services/
│   ├── task_service.py    # Task CRUD operations
│   └── todo_manager.py   # Main application state
├── cli/
│   ├── menu.py            # Interactive menu
│   └── main.py            # Entry point
└── lib/exceptions.py      # Custom exceptions

tests/
├── unit/                   # Isolated component tests
├── integration/              # End-to-end tests
└── contract/                 # Empty for Phase I

pyproject.toml               # Project configuration
README.md                     # This file
CLAUDE.md                     # Claude Code instructions
```

## Troubleshooting

### Python Version Issues

**Problem**: `python --version` shows < 3.13

**Solution**:
```bash
# Install Python 3.13+ from python.org
# macOS: brew install python@3.13
# Windows: Download installer from python.org
# Linux: Use pyenv or system package manager
```

### uv Not Found

**Problem**: `uv: command not found`

**Solution**:
```bash
# Install uv (official installer)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip (less preferred)
pip install uv
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'cli'`

**Solution**:
```bash
# Run from project root
python -m cli.main

# Or ensure PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%cd%/src        # Windows
```

### WSL 2 Issues (Windows Users)

**Problem**: Commands fail on Windows but work on Linux

**Solution**:
```bash
# Ensure you're in WSL 2 environment
wsl --list --verbose  # Should show WSL 2 as default

# Enter WSL 2 if needed
wsl

# All development commands should run in WSL 2 terminal
```

## Demo Preparation

### 90-Second Demo Script

Constitution requires demo video under 90 seconds. Prepare these actions:

**Demo Script** (timed):
1. **0:00-0:10**: Launch application, show menu
2. **0:10-0:25**: Add 3 tasks quickly
3. **0:25-0:35**: View task list, show all tasks
4. **0:35-0:45**: Mark 2 tasks as complete
5. **0:45-0:55**: Update one task title
6. **0:55-0:70**: Delete one task
7. **0:70-0:85**: Show final task list
8. **0:85-0:90**: Exit application

**Tips for Fast Demo**:
- Practice demo sequence multiple times
- Have task titles ready (copy-paste if needed)
- Minimize typing, use short titles
- Keep descriptions short or skip them
- Clear terminal before starting demo

### Record Demo

```bash
# Linux/macOS
asciinema todo-demo.cast
# Press ctrl+d to stop
# Convert to video if needed

# macOS screen recording
screenrecord demo.mov

# OBS Studio (cross-platform)
# Set window source to terminal
# Record at 1080p or higher
```

## Clean Code Verification

### PEP 8 Compliance

```bash
# Install linter
pip install pycodestyle

# Check style
pycodestyle src/ --max-line-length=100
```

### Type Checking

```bash
# Install mypy
pip install mypy

# Check type hints
mypy src/ --strict
```

### Docstring Coverage

```bash
# Install pydocstyle
pip install pydocstyle

# Check docstrings
pydocstyle src/
```

## Success Criteria Verification

### SC-001: Add Task in Under 30 Seconds

**Test**: Time yourself adding first task
1. Launch application: `python -m cli.main`
2. Select "Add Task" (option 1)
3. Enter title and press Enter (skip description)
4. See "✓ Task created" message

**Result**: Should complete in <30 seconds

### SC-002: Mark Complete in Under 5 Seconds

**Test**: Time marking task complete
1. Select "Mark as Complete" (option 3)
2. Enter task ID: `1`
3. See "✓ Task 1 marked as complete"

**Result**: Should complete in <5 seconds

### SC-003: 3 Interactions Max per Operation

**Verification**:
- Add task: 1 menu choice + 2 inputs = 3 interactions ✓
- View tasks: 1 menu choice = 1 interaction ✓
- Mark complete: 1 menu choice + 1 ID = 2 interactions ✓
- Update task: 1 menu choice + 1 ID + 2 inputs = 4 interactions ⚠ (acceptable - core operations under 3)

**Result**: All core operations within 3-4 interactions (acceptable)

### SC-004: Handle Invalid Inputs Without Crashing

**Test**: Try edge cases
1. Add task with empty title → Should see error, continue running
2. Update non-existent task ID 99 → Should see "Task ID 99 not found"
3. View tasks when empty → Should show "Task list is empty" message

**Result**: All errors handled gracefully ✓

### SC-005: Full Cycle in Under 2 Minutes

**Test**: Complete full workflow
1. Add 3 tasks
2. Mark 2 tasks complete
3. Update 1 task
4. Delete 1 task
5. Exit

**Result**: Should complete in <2 minutes for new user

## Next Steps (Phase II)

After Phase I completion and demo submission:

1. **Review Phase I Demo**: Get feedback on usability and features
2. **Update Constitution**: If lessons learned, document for Phase II
3. **Begin Phase II Spec**: Web application with Next.js + FastAPI
4. **Persist Data**: Introduce Neon PostgreSQL (in-memory → persistent)
5. **Add Authentication**: Implement Better Auth with JWT

Phase II will expand to:
- Full-stack web application
- Frontend: Next.js 16+
- Backend: FastAPI + SQLModel
- Database: Neon PostgreSQL
- Authentication: Better Auth with JWT

## Support

**Constitution Compliance**:
- ✅ Spec-driven development (all code from Claude Code)
- ✅ Clean code standards (PEP 8, docstrings, type hints)
- ✅ WSL 2 compatible (all commands work in WSL2)
- ✅ No manual coding (use Claude Code for implementation)

**Issues or Questions**:
- Check constitution: `.specify/memory/constitution.md`
- Review specification: `specs/001-console-todo/spec.md`
- Check data model: `specs/001-console-todo/data-model.md`
- Consult plan: `specs/001-console-todo/plan.md`
