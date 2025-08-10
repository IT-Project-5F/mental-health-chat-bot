# Mental Health Chat Bot

A web application with a React frontend and FastAPI backend for mental health support.

## Project Structure

```
mental-health-chat-bot/
├── client/          # React frontend (Vite + TypeScript)
├── server/          # FastAPI backend (Python)
└── docker-compose.yml
```

## URLs

- **Frontend**: http://localhost:5174 (development) / http://localhost:3000 (production Docker)
- **Backend API**: http://localhost:5001

## Development Setup

### Option 1: Development with Hot Reloading (Recommended)

```bash
# Run with hot reloading enabled
docker-compose -f docker-compose.dev.yml up --build

# Your local file changes will automatically reflect in the browser
# Frontend: http://localhost:5174
# Backend: http://localhost:5001
```

### Option 2: Production Build with Docker Compose

```bash
# Build and start both services (production mode)
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### Option 3: Run with Docker Individually

#### Build and Run Frontend

```bash
cd client
docker build -t mental-health-client .
docker run -p 3000:80 mental-health-client
```

#### Build and Run Backend

```bash
cd server
docker build -t mental-health-server .
docker run -p 5001:5001 mental-health-server
```
