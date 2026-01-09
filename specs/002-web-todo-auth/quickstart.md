# Quickstart Guide: Phase II - Full-Stack Web Todo App with Authentication

**Feature**: Phase II - Full-Stack Web Todo App with Authentication
**Created**: 2026-01-08
**Status**: Complete

## Development Environment Setup

### Prerequisites
- Node.js 18+ (for frontend development)
- Python 3.13+ (for backend development)
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git
- npm or yarn package manager

### Backend Setup (FastAPI)

1. **Create virtual environment and install dependencies:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create `.env` file in the backend directory:
```env
DATABASE_URL="postgresql://username:password@localhost:5432/todoapp"
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
BETTER_AUTH_SECRET="your-better-auth-secret"
NEON_DATABASE_URL="your-neon-database-url"
```

3. **Run database migrations:**
```bash
alembic upgrade head
```

4. **Start the backend server:**
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup (Next.js)

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Set up environment variables:**
Create `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:8000/auth"
BETTER_AUTH_SECRET="your-better-auth-secret"
```

3. **Start the development server:**
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

## Database Schema

The application uses PostgreSQL with the following main tables:

- `users`: Stores user account information
- `tasks`: Stores todo tasks linked to users

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Backend Deployment
1. Deploy to your preferred Python hosting (e.g., Heroku, AWS, GCP)
2. Set environment variables in deployment environment
3. Run database migrations as part of deployment process

### Frontend Deployment
1. Deploy to Vercel for optimal Next.js experience
2. Set environment variables in Vercel dashboard
3. Configure custom domain if needed

## Common Issues and Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correctly set
- Check that PostgreSQL server is running
- Ensure proper network access to database

### Authentication Issues
- Confirm JWT secret keys match between frontend and backend
- Verify Better Auth is properly configured
- Check that CORS settings allow frontend domain

### Frontend Build Issues
- Ensure all dependencies are installed
- Verify environment variables are properly set
- Check TypeScript compilation errors

## Development Workflow

1. Make changes to code
2. Test functionality locally
3. Run tests to ensure no regressions
4. Commit changes with descriptive messages
5. Push to version control
6. Deploy to staging environment for further testing
7. Deploy to production when ready