"""
Authentication API Module

This module provides API endpoints for user authentication, including:
- User registration
- User login and token generation
- User profile retrieval

It uses FastAPI's OAuth2 with Password flow for authentication and JWT tokens
for secure session management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel, EmailStr

from app.db.database import get_db
from app.db.models import User
from app.core.auth import (
    AuthConfig,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()


# Request and response models
class Token(BaseModel):
    """
    Token response model.

    Attributes:
        access_token (str): JWT access token
        token_type (str): Token type (e.g., "bearer")
        user_id (int): ID of the authenticated user
        username (str): Username of the authenticated user
    """

    access_token: str
    token_type: str
    user_id: int
    username: str


class UserCreate(BaseModel):
    """
    User registration request model.

    Attributes:
        username (str): Unique username for the new user
        email (EmailStr): Valid email address for the new user
        password (str): Password for the new user
        full_name (Optional[str]): Optional full name of the user
    """

    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """
    User response model for API responses.

    Attributes:
        id (int): User ID
        username (str): Username
        email (str): Email address
        full_name (Optional[str]): Full name if provided
    """

    id: int
    username: str
    email: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """
    User login request model.

    Attributes:
        username (str): Username for login
        password (str): Password for login
    """

    username: str
    password: str


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get a user by their username.

    Args:
        db (Session): Database session
        username (str): Username to search for

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        db (Session): Database session
        email (str): Email address to search for

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> UserResponse:
    """
    Create a new user in the database.

    Args:
        db (Session): Database session
        user (UserCreate): User data for creation

    Returns:
        UserResponse: The newly created user data (without password)
    """
    # Hash the password
    hashed_password = AuthConfig.get_password_hash(user.password)

    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=True,
        preferences={},
    )

    # Add to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    This endpoint allows new users to register with a username, email, and password.
    It checks if the username or email is already taken before creating the user.

    Args:
        user (UserCreate): User registration data
        db (Session): Database session

    Returns:
        UserResponse: The newly created user data (without password)

    Raises:
        HTTPException: If username or email is already registered
    """
    # Check if username exists
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    return create_user(db, user)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login and get access token.

    This endpoint authenticates a user with username and password,
    and returns a JWT access token for subsequent authenticated requests.

    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials
        db (Session): Database session

    Returns:
        Token: Access token and user information

    Raises:
        HTTPException: If authentication fails
    """
    # Get user by username
    user = get_user_by_username(db, form_data.username)

    # Check if user exists and password is correct
    if not user or not AuthConfig.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthConfig.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # Return token and user info
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile.

    This endpoint returns the profile information of the currently authenticated user.

    Args:
        current_user (User): Current authenticated user from token

    Returns:
        UserResponse: User profile information
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name
    )
