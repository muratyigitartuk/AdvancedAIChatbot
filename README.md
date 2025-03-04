# 🤖 Advanced AI Chatbot

A full-stack web application exploring the frontiers of AI-assisted communication, demonstrating modern software development practices and machine learning integration.

## ✨ Project Features

### 🌟 Core Functionality
- **💬 Interactive Chatbot**: Basic conversational interface
- **📜 Conversation Tracking**: Store and retrieve user chat history
- **🔐 Secure Authentication**: JWT-based user management
- **🌐 OpenAI API Integration**: Foundational AI-powered responses

### 🧠 AI Exploration
- **🤖 OpenAI Language Model**: Basic natural language processing
- **📊 Contextual Understanding**: Preliminary conversation context tracking
- **🌱 Recommendation Engine**: Simple topic-based suggestions
- **🔍 Learning Prototype**: Exploring AI interaction patterns

### 🎨 User Experience
- **⚛️ Responsive Frontend**: Modern React.js interface
- **🌓 Theme Flexibility**: Light and dark mode support
- **📱 Adaptive Design**: Responsive across devices

## 🛠️ Technical Architecture

### Backend
- **🐍 Framework**: Python with FastAPI
- **💾 Database**: PostgreSQL
- **🔑 Authentication**: JWT (JSON Web Tokens)
- **🧠 AI Layer**: OpenAI GPT Integration
- **🚀 Async Processing**: Background task management

### Frontend
- **⚛️ Framework**: React.js with Hooks
- **🎨 UI Components**: Modern, responsive design
- **🌐 State Management**: React Context API
- **📡 API Communication**: Axios

### DevOps & Infrastructure
- **📦 Containerization**: Docker
- **☸️ Orchestration**: Kubernetes configuration
- **🌐 Web Server**: Nginx
- **🔄 CI/CD**: GitHub Actions workflow

## 🚀 Project Vision

This project represents a learning journey in:
- Full-stack web development
- AI and machine learning exploration
- Modern software architecture
- DevOps and cloud technologies

### 🔮 Future Exploration Goals
- Enhanced AI context understanding
- More sophisticated NLP capabilities
- Advanced recommendation systems
- Improved user personalization

## 🧪 Technical Challenges Addressed

### 🌐 Architectural Complexity
- Microservices design
- Scalable application architecture
- Secure authentication mechanisms

### 🤖 AI Integration Exploration
- OpenAI API interaction
- Basic context tracking
- Foundational recommendation engine

### 🔒 Security Considerations
- JWT authentication
- Environment-based configuration
- Secure API interactions

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis (optional, for caching)
- OpenAI API key
- Docker (optional, for containerization)

### Backend Installation

1. Clone the repository:
   ```
   git clone https://github.com/muratyigitartuk/AdvancedAIChatbot.git
   cd advanced-ai-chatbot
   ```

2. Set up a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```
   alembic upgrade head
   ```

6. Start the backend:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## 🔧 Environment Variables

The application uses the following environment variables:

```
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chatbot_db
DB_USER=postgres
DB_PASSWORD=your_password

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
DEFAULT_MODEL=gpt-3.5-turbo

# Authentication
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚢 Deployment

### Docker Deployment

1. Build the Docker images:
   ```
   docker-compose build
   ```

2. Start the containers:
   ```
   docker-compose up -d
   ```

### Kubernetes Deployment

1. Apply Kubernetes configurations:
   ```
   kubectl apply -f k8s/
   ```

## 📚 API Documentation

Once the application is running, visit `/docs` or `/redoc` for interactive API documentation.

### Key API Endpoints

- **🔐 Authentication**
  - `POST /api/auth/register`: Register a new user
  - `POST /api/auth/token`: Login and get access token
  - `GET /api/auth/me`: Get current user profile

- **💬 Chat**
  - `POST /api/chat`: Send a message to the chatbot
  - `GET /api/user/history`: Get user conversation history
  - `GET /api/recommendations`: Get proactive recommendations

## 📂 Project Structure
```markdown
advanced-ai-chatbot/
├── app/                      # Backend application
│   ├── api/                  # API endpoints
│   │   ├── auth.py           # Authentication routes
│   │   ├── chat.py           # Chat functionality routes
│   │   └── voice.py          # Voice processing routes
│   ├── core/                 # Core functionality
│   │   ├── ai_engine.py      # Main AI processing engine
│   │   ├── auth.py           # Authentication logic
│   │   ├── context.py        # Context management
│   │   └── proactive.py      # Proactive recommendations
│   ├── db/                   # Database models & connections
│   │   ├── database.py       # Database connection
│   │   └── models.py         # SQLAlchemy models
│   ├── services/             # External services integration
│   │   ├── user_profile.py   # User profile management
│   │   └── voice_service.py  # Voice processing service
│   └── utils/                # Utility functions
│       └── helpers.py        # Helper functions
├── frontend/                 # React frontend
│   ├── public/               # Static files
│   └── src/                  # Source code
│       ├── components/       # Reusable components
│       ├── contexts/         # React contexts
│       ├── pages/            # Page components
│       └── App.js            # Main application component
├── config/                   # Configuration files
├── k8s/                      # Kubernetes configurations
├── tests/                    # Test suite
├── .env.example              # Example environment variables
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration
└── README.md                 # Project documentation
```

## 🧪 Testing

### Running Backend Tests

```bash
pytest
```

### Running Frontend Tests

```bash
cd frontend
npm test
```

## 👨‍💻 Development Workflow

### Code Style and Linting

We follow PEP 8 guidelines for Python code. You can check your code with:

```bash
flake8 .
```

### Database Migrations

When changing models, create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes

### Pull Request Process

1. Create a feature/bugfix branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request to the develop branch

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Errors

If you encounter database connection issues:

1. Check that PostgreSQL is running
2. Verify your database credentials in `.env`
3. Ensure the database exists: `createdb chatbot_db`

#### OpenAI API Issues

If AI responses are not working:

1. Verify your OpenAI API key in `.env`
2. Check API usage limits on OpenAI dashboard
3. Ensure internet connectivity

#### JWT Authentication Problems

If authentication is failing:

1. Check that SECRET_KEY is properly set
2. Verify token expiration settings
3. Clear browser cookies and try again

## 🚧 Recent Changes

### 2025-02-28: SQLAlchemy Metadata Conflict Resolution

- Renamed 'metadata' column to 'message_metadata' in Message model
- Updated all references across the codebase
- Fixed potential naming conflicts with SQLAlchemy's Declarative API
- Maintained API contract for external interfaces

## 🔮 Future Enhancements

- **🌐 Multi-language Support**: Add support for multiple languages
- **😊 Sentiment Analysis**: Analyze user sentiment to adapt responses
- **🔌 Integration with External APIs**: Weather, news, calendar, etc.
- **📊 Advanced Analytics**: Dashboard for conversation insights
- **📱 Mobile App**: React Native mobile application

## 📚 Learning Objectives

- Practical full-stack development
- AI integration techniques
- Modern web technologies
- DevOps and deployment strategies

## 📜 License

MIT License - Open-source and educational project

## 👨‍💻 About the Developer

**Murat Yigit Artuk**
- 🎓 Aspiring Software Engineering Student
- 🌟 Passionate about Artificial Intelligence, Cloud Computing
- 🚀 Seeking opportunities in innovative software development
- 📍 Targeting Duales Studium Informatik Program

## 📬 Contact

- GitHub: [muratyigitartuk](https://github.com/muratyigitartuk)
- Email: [muratyigitartuk0@gmail.com](mailto:muratyigitartuk0@gmail.com)

## 📚 Detailed API Documentation

### Authentication Endpoints

#### `POST /api/auth/register`
Register a new user in the system.

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "New User"
}
```

**Response (201 Created):**
```json
{
  "id": "user_uuid",
  "username": "newuser",
  "email": "user@example.com",
  "full_name": "New User",
  "created_at": "2025-02-28T19:02:23"
}
```

#### `POST /api/auth/token`
Authenticate and receive an access token.

**Request Body:**
```json
{
  "username": "newuser",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### `GET /api/auth/me`
Get the current user's profile information.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "id": "user_uuid",
  "username": "newuser",
  "email": "user@example.com",
  "full_name": "New User",
  "created_at": "2025-02-28T19:02:23"
}
```

### Chat Endpoints

#### `POST /api/chat`
Send a message to the chatbot and receive a response.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body:**
```json
{
  "message": "Tell me about artificial intelligence",
  "context_id": "optional_conversation_id",
  "metadata": {
    "source": "web",
    "device_info": "Chrome/Windows"
  }
}
```

**Response (200 OK):**
```json
{
  "id": "message_uuid",
  "content": "Artificial intelligence (AI) refers to...",
  "created_at": "2025-02-28T19:05:23",
  "context_id": "conversation_uuid",
  "metadata": {
    "source": "web",
    "device_info": "Chrome/Windows",
    "tokens_used": 150,
    "model": "gpt-3.5-turbo"
  }
}
```

#### `GET /api/user/history`
Retrieve the user's conversation history.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters:**
- `limit` (optional): Maximum number of conversations to return
- `offset` (optional): Pagination offset
- `start_date` (optional): Filter by start date
- `end_date` (optional): Filter by end date

**Response (200 OK):**
```json
{
  "conversations": [
    {
      "id": "conversation_uuid",
      "title": "Conversation about AI",
      "created_at": "2025-02-28T19:00:23",
      "updated_at": "2025-02-28T19:10:23",
      "messages": [
        {
          "id": "message_uuid1",
          "role": "user",
          "content": "Tell me about artificial intelligence",
          "created_at": "2025-02-28T19:05:23"
        },
        {
          "id": "message_uuid2",
          "role": "assistant",
          "content": "Artificial intelligence (AI) refers to...",
          "created_at": "2025-02-28T19:05:30"
        }
      ]
    }
  ],
  "total": 10,
  "limit": 10,
  "offset": 0
}
```

#### `GET /api/recommendations`
Get proactive recommendations based on user's conversation history.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "recommendations": [
    {
      "id": "rec_uuid1",
      "title": "Learn more about Machine Learning",
      "description": "Based on your interest in AI, you might want to explore machine learning concepts.",
      "relevance_score": 0.92,
      "created_at": "2025-02-28T19:15:23"
    },
    {
      "id": "rec_uuid2",
      "title": "Explore Natural Language Processing",
      "description": "NLP is a key component of modern AI systems like chatbots.",
      "relevance_score": 0.85,
      "created_at": "2025-02-28T19:15:23"
    }
  ]
}
```

## 💻 Code Examples

### Backend Examples

#### Sending a Message to the Chatbot (Python)

```python
import requests
import json

# Configuration
API_URL = "http://localhost:8000"
TOKEN = "your_access_token"

# Headers
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Send a message to the chatbot
def send_message(message, context_id=None):
    endpoint = f"{API_URL}/api/chat"

    payload = {
        "message": message,
        "metadata": {
            "source": "python_client",
            "device_info": "Python/Script"
        }
    }

    if context_id:
        payload["context_id"] = context_id

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage
response = send_message("Tell me about machine learning")
print(json.dumps(response, indent=2))

# Continue the conversation
if response and "context_id" in response:
    follow_up = send_message("How is it different from deep learning?", response["context_id"])
    print(json.dumps(follow_up, indent=2))
```

#### User Authentication (Python)

```python
import requests

# Configuration
API_URL = "http://localhost:8000"

# Register a new user
def register_user(username, email, password, full_name):
    endpoint = f"{API_URL}/api/auth/register"

    payload = {
        "username": username,
        "email": email,
        "password": password,
        "full_name": full_name
    }

    response = requests.post(endpoint, json=payload)

    if response.status_code == 201:
        print("User registered successfully!")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Login and get token
def login(username, password):
    endpoint = f"{API_URL}/api/auth/token"

    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(endpoint, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        print("Login successful!")
        return token_data["access_token"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Example usage
new_user = register_user("testuser", "test@example.com", "securepass123", "Test User")
if new_user:
    token = login("testuser", "securepass123")
    print(f"Access Token: {token}")
```

### Frontend Examples

#### React Chat Component

```jsx
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import ChatMessage from './ChatMessage';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [contextId, setContextId] = useState(null);
  const { token } = useAuth();
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Send message to API
  const sendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      created_at: new Date().toISOString()
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(
        '/api/chat',
        {
          message: input,
          context_id: contextId,
          metadata: {
            source: 'web',
            device_info: navigator.userAgent
          }
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      // Add AI response to chat
      const aiMessage = {
        id: response.data.id,
        role: 'assistant',
        content: response.data.content,
        created_at: response.data.created_at
      };

      setMessages(prev => [...prev, aiMessage]);

      // Save context ID for conversation continuity
      if (response.data.context_id) {
        setContextId(response.data.context_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage = {
        id: Date.now().toString(),
        role: 'system',
        content: 'Sorry, there was an error processing your request.',
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map(message => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {loading && (
          <div className="message assistant loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-container" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default Chat;
```

## 🏗️ Architecture Diagrams

### System Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  React Frontend ├──────►  FastAPI Backend├──────►  OpenAI API     │
│                 │      │                 │      │                 │
└────────┬────────┘      └────────┬────────┘      └─────────────────┘
         │                        │
         │                        │
         │                ┌───────▼────────┐
         │                │                │
         └────────────────►  PostgreSQL DB │
                          │                │
                          └────────────────┘
```

### Data Flow Diagram

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │     │               │
│  User Input   ├────►│  Auth Service ├────►│  AI Engine    ├────►│  Response     │
│               │     │               │     │               │     │  Generation   │
└───────┬───────┘     └───────────────┘     └───────┬───────┘     └───────┬───────┘
        │                                           │                     │
        │                                           │                     │
┌───────▼───────┐                          ┌────────▼──────┐     ┌───────▼───────┐
│               │                          │               │     │               │
│  Context      │◄─────────────────────────┤  User Profile │◄────┤  Metadata     │
│  Management   │                          │  Service      │     │  Processing   │
│               │                          │               │     │               │
└───────────────┘                          └───────────────┘     └───────────────┘
```

### Database Schema

```
┌─────────────────────┐       ┌─────────────────────┐
│ User                │       │ Conversation        │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │       │ id (PK)             │
│ username            │       │ user_id (FK)        │
│ email               │       │ title               │
│ hashed_password     │       │ created_at          │
│ full_name           │       │ updated_at          │
│ created_at          │       └──────────┬──────────┘
└──────────┬──────────┘                  │
           │                             │
           │ 1                         1 ┃
           └─────────────────────────────┫
                                         ┃ *
                                ┌────────▼──────────┐
                                │ Message           │
                                ├─────────────────────┤
                                │ id (PK)             │
                                │ conversation_id (FK)│
                                │ role                │
                                │ content             │
                                │ message_metadata    │
                                │ created_at          │
                                └─────────────────────┘
```

## 🤝 Contributing Guide

We welcome contributions to the Advanced AI Chatbot project! This guide will help you get started with the contribution process.

### Getting Started

1. **Fork the Repository**
   - Click the "Fork" button at the top right of the repository page
   - This creates a copy of the repository in your GitHub account

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/AdvancedAIChatbot.git
   cd AdvancedAIChatbot
   ```

3. **Add the Original Repository as Upstream**
   ```bash
   git remote add upstream https://github.com/muratyigitartuk/AdvancedAIChatbot.git
   ```

### Development Workflow

1. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write code that follows the project's coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Feature: Brief description of your changes"
   ```

4. **Pull Latest Changes from Upstream**
   ```bash
   git pull upstream main
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch and submit the pull request with a clear description

### Code Standards

- Follow PEP 8 for Python code
- Use ESLint rules for JavaScript/React code
- Write meaningful commit messages following conventional commits format
- Include docstrings for all functions, classes, and modules
- Maintain test coverage for new code

### Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting a pull request
- Consider edge cases and error scenarios

### Documentation

- Update README.md with new features or changes
- Document new API endpoints
- Add inline comments for complex logic

### Review Process

1. All pull requests require at least one review
2. Address all review comments
3. CI checks must pass before merging
4. Maintainers will merge approved pull requests

### Issue Reporting

If you find a bug or have a feature request:

1. Check if the issue already exists
2. Create a new issue with a descriptive title
3. Include steps to reproduce for bugs
4. Add relevant labels

Thank you for contributing to the Advanced AI Chatbot project!!
