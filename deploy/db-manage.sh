#!/bin/bash

# Database Management Script for This Is Me Backend

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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

COMMAND=${1:-help}

case $COMMAND in
    migrate)
        echo -e "${BLUE}🔄 Running database migrations...${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py migrate
        echo -e "${GREEN}✅ Migrations completed${NC}"
        ;;
    
    makemigrations)
        echo -e "${BLUE}🔄 Creating new migrations...${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py makemigrations
        echo -e "${GREEN}✅ Migrations created${NC}"
        ;;
    
    shell)
        echo -e "${BLUE}🐚 Opening Django shell...${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py shell
        ;;
    
    dbshell)
        echo -e "${BLUE}🐚 Opening database shell...${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py dbshell
        ;;
    
    createsuperuser)
        echo -e "${BLUE}👤 Creating superuser...${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py createsuperuser
        ;;
    
    backup)
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo -e "${BLUE}💾 Creating database backup: $BACKUP_FILE${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec -T db pg_dump -U ${DB_USER:-postgres} ${DB_NAME:-this_is_me_db} > $BACKUP_FILE
        echo -e "${GREEN}✅ Backup saved to $BACKUP_FILE${NC}"
        ;;
    
    restore)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Please provide backup file path${NC}"
            echo "Usage: ./db-manage.sh restore <backup-file.sql>"
            exit 1
        fi
        echo -e "${YELLOW}⚠️  This will restore the database from $2${NC}"
        echo -e "${YELLOW}⚠️  All current data will be replaced!${NC}"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" == "yes" ]; then
            echo -e "${BLUE}🔄 Restoring database...${NC}"
            cat $2 | $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec -T db psql -U ${DB_USER:-postgres} ${DB_NAME:-this_is_me_db}
            echo -e "${GREEN}✅ Database restored${NC}"
        else
            echo -e "${YELLOW}Restore cancelled${NC}"
        fi
        ;;
    
    reset)
        echo -e "${RED}⚠️  WARNING: This will delete ALL data in the database!${NC}"
        read -p "Are you absolutely sure? (type 'DELETE' to confirm): " confirm
        if [ "$confirm" == "DELETE" ]; then
            echo -e "${BLUE}🗑️  Resetting database...${NC}"
            $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py flush --noinput
            echo -e "${GREEN}✅ Database reset${NC}"
        else
            echo -e "${YELLOW}Reset cancelled${NC}"
        fi
        ;;
    
    init)
        echo -e "${BLUE}🔧 Initializing database objects...${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec backend python manage.py initialize_objects
        echo -e "${GREEN}✅ Database initialized${NC}"
        ;;
    
    status)
        echo -e "${BLUE}📊 Database Status:${NC}"
        $DOCKER_COMPOSE_CMD -f docker-compose.prod.yml exec db psql -U ${DB_USER:-postgres} -d ${DB_NAME:-this_is_me_db} -c "\dt"
        ;;
    
    help|*)
        echo "Database Management Commands:"
        echo ""
        echo "  migrate           Run database migrations"
        echo "  makemigrations    Create new migration files"
        echo "  shell             Open Django Python shell"
        echo "  dbshell           Open PostgreSQL shell"
        echo "  createsuperuser   Create a Django admin superuser"
        echo "  backup            Create a database backup"
        echo "  restore <file>    Restore database from backup file"
        echo "  reset             Delete all data (requires confirmation)"
        echo "  init              Initialize database objects"
        echo "  status            Show database tables"
        echo "  help              Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./db-manage.sh migrate"
        echo "  ./db-manage.sh backup"
        echo "  ./db-manage.sh restore backup_20250101_120000.sql"
        ;;
esac

