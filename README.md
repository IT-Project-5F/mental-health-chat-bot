# Mental Health Chat Bot

An intelligent RAG (Retrieval-Augmented Generation) chatbot system for mental health services information with **continuous conversation support**. Built with React frontend, FastAPI backend, PostgreSQL database with pgvector for semantic search, and OpenAI integration.

## ✨ Features

- 🤖 **Continuous Conversations**: Maintain context across multiple messages
- 🔍 **RAG-Powered Responses**: Semantic search through mental health services database
- 💬 **Session Management**: Create and manage chat sessions
- 📝 **Chat History**: View complete conversation history
- 🌐 **RESTful API**: Well-documented FastAPI endpoints
- 🗄️ **Vector Database**: PostgreSQL with pgvector for fast similarity search

## 🌐 URLs & Endpoints

- **Frontend**: http://localhost:5174 (dev) / http://localhost:3000 (prod)
- **Backend API**: http://localhost:5001
- **API Documentation**: http://localhost:5001/docs
- **Health Check**: http://localhost:5001/health
- **Chat Endpoints**:
  - `POST /api/chat` - Send messages (with optional session_id)
  - `POST /api/sessions` - Create new chat session
  - `GET /api/sessions/{session_id}/history` - Get chat history
- **Database**: PostgreSQL with pgvector on port 5432

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
# Database Configuration
POSTGRES_USER=mental_health_user
POSTGRES_PASSWORD=password
POSTGRES_DB=mental_health_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# OpenAI Configuration (Required for RAG)
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Development Setup (Recommended)

```bash
# Start with hot reloading and automatic database setup
docker-compose -f docker-compose.dev.yml up --build

# Access the application
# Frontend: http://localhost:5174
# Backend API: http://localhost:5001
# API Docs: http://localhost:5001/docs
```

### 3. Production Setup

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Postman Workspace

https://www.postman.com/winter-satellite-205821/mental-health-chatbot/overview

### Using the API Documentation

Visit http://localhost:5001/docs to interact with the API through Swagger UI.

## 🗄️ Database Information

The system automatically sets up:

- **PostgreSQL**: With pgvector extension for vector operations
- **MentalHealthRawData**: 599+ mental health service records
- **MentalHealthEmbeddings**: Pre-computed embeddings for semantic search
- **Vector Index**: IVFFLAT index for fast similarity search

### Database Connection

```bash
# Connect to database
docker exec -it mental_health_postgres_dev psql -U mental_health_user -d mental_health_db

# Check data
SELECT COUNT(*) FROM MentalHealthRawData;
SELECT COUNT(*) FROM MentalHealthEmbeddings;
```

## 🛠️ Development

### Manual Development (Without Docker)

#### Backend Setup

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

#### Frontend Setup

```bash
cd client
npm install
npm run dev
```

### Project Structure Details

- **`server/rag_service.py`**: Core RAG implementation with vector search
- **`server/main.py`**: FastAPI endpoints and CORS configuration
- **`server/init-db/`**: Database initialization scripts
- **`client/`**: React frontend with TypeScript
- **`*.csv`**: Mental health services data and embeddings

### Reset Everything

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```
