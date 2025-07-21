#!/bin/bash

# Docker Installation Script for Ubuntu
# This script automates the installation of Docker CE and Docker Compose

set -e  # Exit on any error

echo "=== Docker Installation Script for Ubuntu ==="
echo "This script will install Docker CE and Docker Compose"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root for security reasons"
   echo "Please run as a regular user with sudo privileges"
   exit 1
fi

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install required dependencies
echo "Installing required dependencies..."
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common

# Add Docker's official GPG key
echo "Adding Docker's official GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "Adding Docker repository..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package lists again
echo "Updating package lists with Docker repository..."
sudo apt update

# Install Docker CE
echo "Installing Docker CE..."
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Start and enable Docker service
echo "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group
echo "Adding user $USER to docker group..."
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
echo
echo "=== Verifying Installation ==="
docker --version
docker-compose --version

# Test Docker installation
echo
echo "Testing Docker installation..."
sudo docker run hello-world

echo
echo "=== Installation Complete ==="
echo "Docker and Docker Compose have been successfully installed!"
echo
echo "IMPORTANT: You need to log out and log back in (or restart your system)"
echo "for the group membership changes to take effect."
echo "After that, you can run Docker commands without sudo."
echo
echo "To test without logout, you can use: sudo docker run hello-world"
