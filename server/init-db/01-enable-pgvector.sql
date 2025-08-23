-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a user if not exists (optional, for additional security)
-- This is handled by Docker environment variables

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mental_health_db TO mental_health_user;