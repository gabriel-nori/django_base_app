#!/bin/bash

# Production Restart Script for This Is Me Backend

set -e  # Exit on error

echo "🔄 Restarting This Is Me Backend..."

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

echo -e "${BLUE}🐳 Restarting Docker containers...${NC}"
$DOCKER_COMPOSE_CMD -f docker-compose.prod.yml restart

echo ""
echo -e "${GREEN}✅ Application restarted successfully!${NC}"
echo ""
echo "📊 Container Status:"
$DOCKER_COMPOSE_CMD -f docker-compose.prod.yml ps
echo ""
echo "📝 To view logs: $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml logs -f backend"

