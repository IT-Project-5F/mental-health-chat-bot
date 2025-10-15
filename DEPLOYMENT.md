# Production Deployment Guide

## Overview

Your app will be accessible at:

- **Frontend**: `https://yourdomain.com`
- **Backend API**: `https://api.yourdomain.com`

**Note:** This project uses a **self-hosted GitHub Actions runner** for deployments. The runner must be installed on your VM to enable automatic deployments via GitHub Actions.

## Setup Instructions

### 1. Install Docker on VM (One-time setup)

Commands vary by cloud provider and OS:

#### AWS EC2 (Amazon Linux)

SSH into your EC2 instance and run:

```bash
# Update system packages
sudo yum update -y

# Install Docker
sudo yum install docker -y

# Start Docker service and enable it to start on boot
sudo systemctl start docker
sudo systemctl enable docker

# Add ec2-user to docker group (so you don't need sudo for docker commands)
sudo usermod -aG docker ec2-user

# IMPORTANT: Log out and log back in for group changes to take effect
exit
```

#### Azure VM (Ubuntu/Debian)

SSH into your Azure VM and run:

```bash
# Update system packages
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Start Docker service and enable it to start on boot
sudo systemctl start docker
sudo systemctl enable docker

# Add azureuser to docker group (so you don't need sudo for docker commands)
sudo usermod -aG docker azureuser

# IMPORTANT: Log out and log back in for group changes to take effect
exit
```

**SSH back into your VM**, then continue:

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Setup Self-Hosted GitHub Runner (One-time setup)

Since this project uses a self-hosted runner, you need to install the GitHub Actions runner on your VM:

1. Go to your GitHub repository → **Settings** → **Actions** → **Runners** → **New self-hosted runner**

2. Follow the instructions provided by GitHub. They will look similar to:

```bash
# Create a folder for the runner
mkdir actions-runner && cd actions-runner

# Download the latest runner package
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure the runner (use the token provided by GitHub)
./config.sh --url https://github.com/yourusername/your-repo --token YOUR_TOKEN_HERE

# Install as a service (so it runs automatically)
sudo ./svc.sh install

# Start the runner service
sudo ./svc.sh start

# Check status
sudo ./svc.sh status
```

3. Verify the runner appears as "Idle" in your GitHub repository's Actions → Runners page

### 3. Create Traefik Network (One-time setup)

```bash
docker network create traefik-public
```

### 4. Add GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions

Add these secrets:

- `DOMAIN_STAGING` = `yourdomain.com` (your actual domain)
- `ACME_EMAIL` = `your-email@example.com` (for SSL certificates)
- `DOCKER_IMAGE_STAGING` = `mental-health-app` (or any name you want)
- All other existing secrets (DATABASE_URL, JWT_SECRET, etc.)

### 5. DNS Configuration

Point these DNS records to your server IP (AWS or Azure):

- A record: `yourdomain.com` → `your-server-ip`
- A record: `api.yourdomain.com` → `your-server-ip`

### 6. Deploy

Push to main branch - GitHub Actions will automatically deploy

## How It Works

### Domain Routing (Traefik)

- Traefik listens on ports 80 (HTTP) and 443 (HTTPS)
- Automatically gets SSL certificates from Let's Encrypt
- Routes traffic based on domain:
  - `yourdomain.com` → client container (port 80)
  - `api.yourdomain.com` → server container (port 5001)

### Environment Variables

The workflow sets these automatically:

- `DOMAIN` - Your domain name
- `ENVIRONMENT=staging` - Tells the app it's in production mode
- `FRONTEND_URL` - Set to `https://yourdomain.com` for CORS

### Client API URL

- **Development**: Uses `http://localhost:5001`
- **Production**: Built with `https://api.yourdomain.com`

## Local Development

Development uses [docker-compose.dev.yml](docker-compose.dev.yml):

```bash
docker-compose -f docker-compose.dev.yml up
```

This keeps localhost URLs for local development.
