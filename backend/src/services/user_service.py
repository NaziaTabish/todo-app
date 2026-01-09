"""User service for Todo application."""

import logging
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..models.user import User, UserCreate, UserUpdate
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a hash for a plain password."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user or not UserService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        logger.info(f"Creating new user with email: {user_create.email}")

        # Hash the password
        hashed_password = UserService.get_password_hash(user_create.password)

        # Create the user object
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        logger.info(f"Successfully created user with ID: {db_user.id}")
        return db_user

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by email."""
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def update_user(session: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Update a user's information."""
        db_user = session.get(User, user_id)
        if not db_user:
            return None

        # Update fields if provided
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.first_name is not None:
            db_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            db_user.last_name = user_update.last_name
        if user_update.password is not None:
            db_user.hashed_password = UserService.get_password_hash(user_update.password)

        # Update timestamp
        db_user.updated_at = datetime.utcnow()

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user