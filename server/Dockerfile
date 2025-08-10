FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 5001
EXPOSE 5001

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]