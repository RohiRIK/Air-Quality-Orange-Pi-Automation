#!/bin/bash

# Update the package list
sudo apt-get update

# Install Docker
if ! [ -x "$(command -v docker)" ]; then
    echo "Docker is not installed. Installing Docker..."
    sudo apt-get install -y docker.io
fi

# Install Docker Compose
if ! [ -x "$(command -v docker-compose)" ]; then
    echo "Docker Compose is not installed. Installing Docker Compose..."
    sudo apt-get install -y docker-compose
fi

# Add the current user to the docker group to avoid using sudo with docker commands
sudo usermod -aG docker ${USER}

echo "Dependencies installed successfully."
