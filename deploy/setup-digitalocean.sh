#!/bin/bash
# PIPA DigitalOcean Deployment Script
# Run this on a fresh Ubuntu 22.04 droplet (4GB+ RAM recommended)
#
# Usage:
#   ssh root@YOUR_DROPLET_IP
#   curl -sSL https://raw.githubusercontent.com/lcerdeira/Pipa/main/deploy/setup-digitalocean.sh | bash

set -e

echo "=== PIPA Deployment ==="

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    apt-get install -y docker-compose-plugin
fi

# Clone repo
echo "Cloning PIPA..."
cd /opt
rm -rf Pipa
git clone https://github.com/lcerdeira/Pipa.git
cd Pipa

# Build frontend image and start services
echo "Starting PIPA services..."
docker compose up -d --build

# Show status
echo ""
echo "=== PIPA is running! ==="
echo "URL: http://$(curl -s ifconfig.me)"
echo ""
echo "To check status:  docker compose ps"
echo "To view logs:     docker compose logs -f"
echo "To stop:          docker compose down"
echo "To restart:       docker compose restart"
