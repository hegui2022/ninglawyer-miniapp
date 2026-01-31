#!/bin/bash

# Setup script for deployment
# This script prepares the environment before deployment

set -e  # Exit on error

echo "======================================"
echo "Starting deployment setup..."
echo "======================================"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend/src"
echo "PYTHONPATH set to: ${PYTHONPATH}"

# Navigate to backend directory
cd backend

echo "Current directory: $(pwd)"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found"
    echo "Creating .env from .env.example..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ".env file created from .env.example"
    else
        echo "Error: .env.example not found"
        exit 1
    fi
fi

echo "Environment configuration: OK"

# Initialize database if needed (optional)
echo "Checking database..."
if [ -f "ninglawyer.db" ]; then
    echo "Database file exists: ninglawyer.db"
else
    echo "Database file not found. Will be created automatically on first run."
fi

# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    echo "Creating logs directory..."
    mkdir -p logs
    echo "Logs directory created"
fi

# Create assets directory if it doesn't exist
if [ ! -d "assets" ]; then
    echo "Creating assets directory..."
    mkdir -p assets/images
    mkdir -p assets/knowledge
    mkdir -p assets/templates
    echo "Assets directories created"
fi

echo "======================================"
echo "Deployment setup completed successfully!"
echo "======================================"

exit 0
