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
