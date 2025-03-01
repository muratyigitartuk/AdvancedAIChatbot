"""
Authentication Tests Module

This module contains tests for the authentication functionality of the advanced
AI chatbot application. It tests various authentication scenarios including:

1. User Registration
   - Successful registration with valid credentials
   - Failed registration attempts with existing usernames or emails

2. User Login
   - Successful login with correct credentials
   - Failed login attempts with incorrect passwords

3. User Authentication
   - Retrieving current user profile with valid token
   - Handling invalid authentication tokens

These tests ensure that the authentication system properly validates user
credentials, manages user sessions, and protects user data with appropriate
security measures.
"""

from fastapi import status

# Removing unused imports
# import pytest
# from sqlalchemy.orm import Session
# from app.core.auth import AuthConfig


def test_register_user(client):
    """Test registering a new user."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure_password",
            "full_name": "New User",
        },
    )
    if response.status_code != status.HTTP_201_CREATED:
        raise AssertionError("Expected status code 201 Created")
    data = response.json()
    if data["username"] != "newuser":
        raise AssertionError("Username mismatch")
    if data["email"] != "newuser@example.com":
        raise AssertionError("Email mismatch")
    if data["full_name"] != "New User":
        raise AssertionError("Full name mismatch")
    if "id" not in data:
        raise AssertionError("ID missing in response")
    if "hashed_password" in data:
        raise AssertionError("Hashed password should not be in response")


def test_register_existing_username(client, test_user):
    """Test registering with an existing username."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",  # Same as test_user fixture
            "email": "different@example.com",
            "password": "secure_password",
        },
    )
    if response.status_code != status.HTTP_400_BAD_REQUEST:
        raise AssertionError("Expected status code 400 Bad Request")
    error_detail = response.json()["detail"]
    expected_error = "already registered"
    if expected_error not in error_detail:
        raise AssertionError(f"Expected '{expected_error}' in error detail")


def test_register_existing_email(client, test_user):
    """Test registering with an existing email."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "differentuser",
            "email": "test@example.com",  # Same as test_user fixture
            "password": "secure_password",
        },
    )
    if response.status_code != status.HTTP_400_BAD_REQUEST:
        raise AssertionError("Expected status code 400 Bad Request")
    error_detail = response.json()["detail"]
    expected_error = "already registered"
    if expected_error not in error_detail:
        raise AssertionError(f"Expected '{expected_error}' in error detail")


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/api/auth/token",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")
    data = response.json()
    if "access_token" not in data:
        raise AssertionError("Access token missing in response")
    if data["token_type"] != "bearer":
        raise AssertionError("Token type should be 'bearer'")
    if data["username"] != "testuser":
        raise AssertionError("Username mismatch")


def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    response = client.post(
        "/api/auth/token",
        data={"username": "testuser", "password": "wrong_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if response.status_code != status.HTTP_401_UNAUTHORIZED:
        raise AssertionError("Expected status code 401 Unauthorized")
    error_detail = response.json()["detail"]
    expected_error = "Incorrect username or password"
    if expected_error not in error_detail:
        raise AssertionError(f"Expected '{expected_error}' in error detail")


def test_get_current_user(client, test_user_token):
    """Test getting current user profile."""
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {test_user_token}"})
    if response.status_code != status.HTTP_200_OK:
        raise AssertionError("Expected status code 200 OK")
    data = response.json()
    if data["username"] != "testuser":
        raise AssertionError("Username mismatch")
    if data["email"] != "test@example.com":
        raise AssertionError("Email mismatch")
    if data["full_name"] != "Test User":
        raise AssertionError("Full name mismatch")


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token."""
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid_token"})
    if response.status_code != status.HTTP_401_UNAUTHORIZED:
        raise AssertionError("Expected status code 401 Unauthorized")
    error_detail = response.json()["detail"]
    expected_error = "Could not validate credentials"
    if expected_error not in error_detail:
        raise AssertionError(f"Expected '{expected_error}' in error detail")
