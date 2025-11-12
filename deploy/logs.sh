#!/bin/bash

# Production Logs Script for This Is Me Backend

# Colors for output
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

# Default to following all logs
SERVICE=${1:-}
FOLLOW=${2:--f}

if [ -z "$SERVICE" ]; then
    echo -e "${BLUE}📝 Showing logs for all services...${NC}"
    $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml logs $FOLLOW
else
    echo -e "${BLUE}📝 Showing logs for $SERVICE...${NC}"
    $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml logs $FOLLOW $SERVICE
fi

