#!/bin/bash

# Production startup script for automation service
echo "Starting Automation Service..."

# Check if credentials file exists
if [ ! -f "credentials.json" ]; then
    echo "Warning: credentials.json not found. Google Sheets integration will be disabled."
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please copy .env to .env and configure your API credentials."
    exit 1
fi

# Start the service
exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1