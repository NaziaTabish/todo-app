# Todo Application - Phase II: Full-Stack Web App with Authentication

## Overview

This is the second phase of the Todo Application project, transforming the console-based application into a modern full-stack web application with multi-user authentication and persistent storage.

### Features
- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Create, read, update, delete, and mark tasks as complete
- **Multi-User Support**: Each user has their own isolated task list
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern Tech Stack**: Next.js frontend with FastAPI backend

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Authentication**: Custom auth utilities with JWT

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT with custom implementation
- **Dependencies**: uvicorn, passlib, python-jose

## Architecture

The application follows a clean architecture pattern:

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Next.js pages
│   ├── services/       # API clients and auth utilities
│   ├── types/          # TypeScript type definitions
│   └── context/        # React context providers
└── ...

backend/
├── src/
│   ├── models/         # SQLModel database models
│   ├── services/       # Business logic
│   ├── api/            # API endpoints
│   └── database/       # Database connection setup
└── ...
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.13+
- PostgreSQL (or access to Neon Serverless PostgreSQL)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory:
```env
DATABASE_URL="postgresql://username:password@localhost:5432/todoapp"
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
BETTER_AUTH_SECRET="your-better-auth-secret"
NEON_DATABASE_URL="your-neon-database-url"
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:8000/auth"
BETTER_AUTH_SECRET="your-better-auth-secret"
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### Tasks API
- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Project Structure

The project is organized by feature in the `specs/` directory:
- `specs/001-console-todo/` - Phase I: Console application
- `specs/002-web-todo-auth/` - Phase II: Full-stack web application with authentication

## Success Criteria

1. **SC-001**: New users can register, log in, and create their first task within 2 minutes
2. **SC-002**: Authenticated users can perform all 5 CRUD operations with 2 or fewer clicks each
3. **SC-003**: The application supports at least 100 concurrent users without performance degradation
4. **SC-004**: API endpoints return responses within 2 seconds under normal load conditions
5. **SC-005**: Users cannot access or modify other users' tasks regardless of direct API access attempts
6. **SC-006**: The web interface is fully responsive and usable on desktop, tablet, and mobile devices

## Next Steps

- [ ] Add end-to-end tests for critical user flows
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend API to hosting provider
- [ ] Connect to Neon PostgreSQL database in production

## License

This project is licensed under the MIT License.