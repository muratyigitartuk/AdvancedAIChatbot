"""
Authentication Module

This module provides JWT-based authentication functionality for the application.
It includes password hashing, token generation and validation, and user authentication.

The module uses:
- FastAPI's OAuth2 with Password flow for authentication
- JWT (JSON Web Tokens) for secure token-based authentication
- Passlib for password hashing with bcrypt
- SQLAlchemy for database interactions

Environment variables:
- JWT_SECRET_KEY: Secret key for signing JWT tokens
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.database import get_db
import os

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configure OAuth2 with token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "DO_NOT_USE_THIS_IN_PRODUCTION_REPLACE_IT_WITH_YOUR_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class AuthConfig:
    """
    Authentication configuration and utility methods.
    
    This class provides static methods for password verification, password hashing,
    and JWT token creation and validation.
    """
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            plain_password (str): The plain text password to verify
            hashed_password (str): The hashed password to compare against
            
        Returns:
            bool: True if the password matches the hash, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password for secure storage.
        
        Args:
            password (str): The plain text password to hash
            
        Returns:
            str: The hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a new JWT access token.
        
        Args:
            data (Dict[str, Any]): The data to encode in the token, typically includes user ID
            expires_delta (Optional[timedelta], optional): Custom expiration time. 
                Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.
                
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependency to get the current authenticated user from a JWT token.
    
    This function validates the JWT token, extracts the user ID, and fetches
    the corresponding user from the database.
    
    Args:
        token (str): The JWT token from the Authorization header
        db (Session): Database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If the token is invalid or the user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    # Get the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get the current active user.
    
    This function checks if the authenticated user is active.
    
    Args:
        current_user (User): The authenticated user from get_current_user
        
    Returns:
        User: The active authenticated user
        
    Raises:
        HTTPException: If the user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
        
    return current_user
