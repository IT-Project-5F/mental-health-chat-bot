FROM python:3.11-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libc6-dev \
    libstdc++-10-dev \
    curl \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (needed for fastuuid)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application

COPY . . 

# Expose port (adjust if needed)
EXPOSE 5001

# Run your FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
