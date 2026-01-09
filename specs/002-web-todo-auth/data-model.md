# Data Model: Phase II - Full-Stack Web Todo App with Authentication

**Feature**: Phase II - Full-Stack Web Todo App with Authentication
**Created**: 2026-01-08
**Status**: Complete

## Entity: User

**Description**: Represents an authenticated user in the system

**Fields**:
- `id`: UUID (primary key, unique, not null)
- `email`: String (unique, not null, validated email format)
- `username`: String (unique, not null, 3-30 characters)
- `hashed_password`: String (not null, min 8 characters when hashed)
- `first_name`: String (optional, max 50 characters)
- `last_name`: String (optional, max 50 characters)
- `created_at`: DateTime (not null, default now)
- `updated_at`: DateTime (not null, default now, auto-update)
- `is_active`: Boolean (not null, default true)
- `is_verified`: Boolean (not null, default false)

**Validation Rules**:
- Email must be valid email format
- Username must be 3-30 alphanumeric characters plus underscores/hyphens
- Password must be at least 8 characters when provided
- Email and username must be unique across all users

**Relationships**:
- One-to-many: User → Tasks (user owns multiple tasks)

## Entity: Task

**Description**: Represents a todo item owned by a specific user

**Fields**:
- `id`: UUID (primary key, unique, not null)
- `title`: String (not null, 1-200 characters)
- `description`: Text (optional, max 10000 characters)
- `completed`: Boolean (not null, default false)
- `created_at`: DateTime (not null, default now)
- `updated_at`: DateTime (not null, default now, auto-update)
- `user_id`: UUID (foreign key to User.id, not null)
- `due_date`: DateTime (optional)
- `priority`: Integer (not null, default 1, range 1-3 with 1=highest)

**Validation Rules**:
- Title must be 1-200 characters
- Description must be max 10000 characters if provided
- Priority must be between 1-3
- User_id must reference an existing user
- Completed must be boolean value

**State Transitions**:
- Incomplete (completed=False) ↔ Complete (completed=True)

**Relationships**:
- Many-to-one: Task → User (task belongs to one user)
- User owns multiple tasks

## Entity: Session (Implicit in Better Auth)

**Description**: Represents an active user session (handled by Better Auth)

**Fields**:
- `token`: JWT String (not null)
- `user_id`: UUID (foreign key to User.id, not null)
- `expires_at`: DateTime (not null)
- `created_at`: DateTime (not null, default now)
- `last_accessed`: DateTime (not null, default now, auto-update)

**Note**: This entity is primarily managed by Better Auth, with custom extensions as needed.

## Indexes

**User Table**:
- Primary: id (UUID)
- Unique: email (for login)
- Unique: username (for identification)

**Task Table**:
- Primary: id (UUID)
- Foreign: user_id (for user isolation queries)
- Composite: (user_id, created_at) for efficient user task listings
- Index: completed (for filtering completed/incomplete tasks)

## Constraints

**Referential Integrity**:
- Task.user_id must reference valid User.id
- Cascade delete: If user is deleted, all their tasks are deleted

**Data Consistency**:
- User email uniqueness enforced at database level
- User username uniqueness enforced at database level
- Task title non-empty constraint