#!/bin/bash

# Production Stop Script for Django Base App

set -e  # Exit on error

echo "🛑 Stopping Django Base App..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

echo -e "${BLUE}🐳 Stopping Docker containers...${NC}"
$DOCKER_COMPOSE_CMD -f docker-compose.prod.yml down

echo ""
echo -e "${GREEN}✅ Application stopped successfully!${NC}"
echo ""
echo "To start again: ./run.sh"

