"""
Authentication Tests Module

This module contains tests for the authentication functionality of the advanced AI chatbot application.
It tests various authentication scenarios including:

1. User Registration
   - Successful registration with valid credentials
   - Failed registration attempts with existing usernames or emails

2. User Login
   - Successful login with correct credentials
   - Failed login attempts with incorrect passwords

3. User Authentication
   - Retrieving current user profile with valid token
   - Handling invalid authentication tokens

These tests ensure that the authentication system properly validates user credentials,
manages user sessions, and protects user data with appropriate security measures.
"""

import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.core.auth import AuthConfig

def test_register_user(client):
    """Test registering a new user"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure_password",
            "full_name": "New User"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data

def test_register_existing_username(client, test_user):
    """Test registering with an existing username"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",  # Same as test_user fixture
            "email": "different@example.com",
            "password": "secure_password"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"]

def test_register_existing_email(client, test_user):
    """Test registering with an existing email"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "differentuser",
            "email": "test@example.com",  # Same as test_user fixture
            "password": "secure_password"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"]

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "testuser"

def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "wrong_password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.json()["detail"]

def test_get_current_user(client, test_user_token):
    """Test getting current user profile"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate credentials" in response.json()["detail"]
