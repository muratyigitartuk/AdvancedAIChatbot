"""
Advanced AI Chatbot API - Main Application Module

This module initializes the FastAPI application, sets up database connections,
configures middleware, and registers API routers. It serves as the entry point
for the entire backend application.

The application provides endpoints for:
- User authentication and profile management
- Chat functionality with AI-powered responses
- Voice processing (speech-to-text and text-to-speech)

Environment variables are loaded from a .env file and used for configuration.
Database tables are automatically created on application startup if they don't exist.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.api import chat, voice, auth
from app.db.database import engine, Base

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Advanced AI Chatbot",
    description="An AI chatbot with personalization, voice support, and proactive recommendations",
    version="0.1.0",
)

# Configure CORS
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Restrict to specific trusted origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])


@app.get("/")
def read_root():
    """
    Root endpoint that provides basic API information.

    Returns:
        dict: A dictionary containing a welcome message and link to documentation
    """
    return {
        "message": "Welcome to the Advanced AI Chatbot API",
        "documentation": "/docs",
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    This endpoint can be used by monitoring tools and load balancers
    to verify that the application is running properly.

    Returns:
        dict: A dictionary with status information
    """
    return {"status": "healthy", "version": app.version}


# Run the application with uvicorn
if __name__ == "__main__":
    """
    Development server entry point.

    This block is executed when the script is run directly.
    In production, the application should be run using a proper ASGI server.
    """
    import uvicorn

    # Create database tables
    Base.metadata.create_all(bind=engine)

    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
