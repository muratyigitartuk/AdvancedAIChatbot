# 🤖 Advanced AI Chatbot

An advanced AI chatbot system capable of storing and recalling user history, providing proactive solutions, and supporting voice interactions. The chatbot learns from each user's past requests, anticipates their needs, and delivers personalized responses.

## ✨ Features

- **🧠 Personalized Responses**: Learns from user interaction history to provide tailored answers
- **🔮 Proactive Recommendations**: Anticipates user needs based on past conversations and context
- **🎤 Voice Support**: Full speech-to-text and text-to-speech capabilities for natural interactions
- **📊 Multi-Modal Support**: Process and respond to various content types including text and voice
- **🏷️ Topic Analysis**: Identifies key topics and entities in conversations to improve understanding
- **⚡ Action System**: Performs actions based on user requests (reminders, notes, etc.)
- **🔐 User Authentication**: Secure JWT-based authentication system
- **📜 Conversation History**: Stores and retrieves past conversations for context awareness
- **🎨 Responsive UI**: Modern React-based interface with light/dark theme support

## 🛠️ Technical Stack

### Backend
- **🐍 Framework**: Python, FastAPI
- **💾 Database**: PostgreSQL for relational data, Redis for caching
- **🔑 Authentication**: JWT (JSON Web Tokens)
- **⏱️ Task Processing**: Celery for asynchronous tasks

### Frontend
- **⚛️ Framework**: React with hooks and context API
- **🎭 UI Library**: Material-UI for responsive components
- **🧩 State Management**: React Context API
- **🌐 HTTP Client**: Axios for API requests

### AI/ML Components
- **🧪 NLP**: Hugging Face Transformers, OpenAI API, NLTK, spaCy
- **🔊 Voice Processing**: Whisper (STT), ElevenLabs (TTS)
- **🧩 Context Management**: Custom context builder with user profile integration

### DevOps
- **📦 Containerization**: Docker
- **☸️ Orchestration**: Kubernetes
- **🌐 Web Server**: Nginx
- **🔄 CI/CD**: GitHub Actions

## 🚀 Setup & Installation

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL
- Redis
- Docker (optional for containerized deployment)

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
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
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

- **🔊 Voice**
  - `POST /api/voice/stt`: Convert speech to text
  - `POST /api/voice/tts`: Convert text to speech

## 📂 Project Structure

```
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

```
pytest
```

### Running Frontend Tests

```
cd frontend
npm test
```

## 🔮 Future Enhancements

- **🌐 Multi-language Support**: Add support for multiple languages
- **😊 Sentiment Analysis**: Analyze user sentiment to adapt responses
- **🔌 Integration with External APIs**: Weather, news, calendar, etc.
- **📊 Advanced Analytics**: Dashboard for conversation insights
- **📱 Mobile App**: React Native mobile application

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Developed by Murat Yigit Artuk

## 📬 Contact

- GitHub: [muratyigitartuk](https://github.com/muratyigitartuk)
- G-Mail: [muratyigitartuk0@gmail.com]
