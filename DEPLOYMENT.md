# Production Deployment Guide

## Overview
Your app will be accessible at:
- **Frontend**: `https://yourdomain.com`
- **Backend API**: `https://api.yourdomain.com`

## Setup Instructions

### 1. Install Docker on EC2 (One-time setup)
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

**SSH back into EC2**, then continue:

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Create Traefik Network (One-time setup)
```bash
docker network create traefik-public
```

### 3. Add GitHub Secrets
Go to your repo → Settings → Secrets and variables → Actions

Add these secrets:
- `DOMAIN_STAGING` = `yourdomain.com` (your actual domain)
- `ACME_EMAIL` = `your-email@example.com` (for SSL certificates)
- `DOCKER_IMAGE_STAGING` = `mental-health-app` (or any name you want)
- All other existing secrets (DATABASE_URL, JWT_SECRET, etc.)

### 4. DNS Configuration
Point these DNS records to your AWS server IP:
- A record: `yourdomain.com` → `your-server-ip`
- A record: `api.yourdomain.com` → `your-server-ip`

### 5. Deploy
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
