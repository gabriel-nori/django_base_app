#!/bin/bash

# Production Build Script for Django Base App

set -e  # Exit on error

echo "🏗️  Building Django Base App for Production..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Check if .env file exists (in deploy folder)
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo -e "${RED}❌ Error: .env file not found in deploy folder${NC}"
    echo "Please create a .env file based on env.prod.example"
    echo "Location: $SCRIPT_DIR/.env"
    exit 1
fi

# Load environment variables
echo -e "${BLUE}📋 Loading environment variables...${NC}"
source "$SCRIPT_DIR/.env"

# Check if required variables are set
required_vars=("SECRET_KEY" "DB_NAME" "DB_USER" "DB_PASS" "ALLOWED_HOSTS")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}❌ Error: $var is not set in .env${NC}"
        exit 1
    fi
done

# Build the Docker image (from project root, with deploy/Dockerfile)
echo -e "${BLUE}🐳 Building Docker image...${NC}"
cd "$PROJECT_ROOT"
docker build -t django-base-app:latest -f deploy/Dockerfile .

echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo ""
echo "To run the application, use: ./run.sh"

