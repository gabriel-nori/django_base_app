#!/bin/bash

# Production Run Script for This Is Me Backend

set -e  # Exit on error

echo "🚀 Starting This Is Me Backend (Production)"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists (in deploy folder)
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found in deploy folder${NC}"
    echo "Please create a .env file based on env.prod.example"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Error: docker-compose is not installed${NC}"
    exit 1
fi

# Use docker compose or docker-compose based on availability
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
fi

# Check if services are already running
if $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  Services are already running${NC}"
    echo "To restart, use: ./restart.sh"
    echo "To stop, use: ./stop.sh"
    exit 0
fi

echo -e "${BLUE}🐳 Starting Docker containers...${NC}"
$DOCKER_COMPOSE_CMD -f docker-compose.prod.yml up -d

echo ""
echo -e "${GREEN}✅ Application started successfully!${NC}"
echo ""
echo "📊 Container Status:"
$DOCKER_COMPOSE_CMD -f docker-compose.prod.yml ps
echo ""
echo "📝 To view logs: $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml logs -f backend"
echo "🛑 To stop: ./stop.sh"
echo "🔄 To restart: ./restart.sh"

