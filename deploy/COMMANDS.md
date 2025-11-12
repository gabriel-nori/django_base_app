# Production Commands Quick Reference

This document provides a quick reference for all production deployment commands.

**Note**: All commands must be run from the `deploy` folder unless otherwise specified.

## 🚀 Setup and Deployment

### Initial Setup
```bash
# Navigate to deploy folder
cd deploy

# 1. Create environment configuration
cp env.prod.example .env
# Edit .env with your settings

# 2. Build the Docker image
./build.sh

# 3. Start the application
./run.sh
```

## 🔄 Application Management

### Start/Stop Services
```bash
./run.sh      # Start all services (backend, database, redis)
./stop.sh     # Stop all services
./restart.sh  # Restart all services
```

### View Logs
```bash
./logs.sh              # View logs for all services
./logs.sh backend      # View logs for backend only
./logs.sh db           # View logs for database only
./logs.sh redis        # View logs for redis only
```

## 💾 Database Management

### Migrations
```bash
./db-manage.sh migrate          # Run pending migrations
./db-manage.sh makemigrations   # Create new migration files
```

### Database Access
```bash
./db-manage.sh shell      # Open Django Python shell
./db-manage.sh dbshell    # Open PostgreSQL shell
./db-manage.sh status     # Show database tables
```

### User Management
```bash
./db-manage.sh createsuperuser  # Create admin user
```

### Backup & Restore
```bash
./db-manage.sh backup                        # Create database backup
./db-manage.sh restore backup_file.sql       # Restore from backup
```

### Initialization & Reset
```bash
./db-manage.sh init   # Initialize database objects
./db-manage.sh reset  # Delete all data (requires confirmation)
```

## 🐳 Docker Commands

### Docker Compose
```bash
# Start services
docker compose -f docker-compose.prod.yml up -d

# Stop services
docker compose -f docker-compose.prod.yml down

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Restart specific service
docker compose -f docker-compose.prod.yml restart backend

# View container status
docker compose -f docker-compose.prod.yml ps

# Remove volumes (deletes all data)
docker compose -f docker-compose.prod.yml down -v
```

### Docker Direct
```bash
# Build image
docker build -t this-is-me-backend:latest -f dockerfile .

# View images
docker images | grep this-is-me

# View running containers
docker ps

# View all containers
docker ps -a

# Container logs
docker logs -f this-is-me-backend

# Execute command in container
docker exec -it this-is-me-backend python manage.py shell

# Container stats
docker stats this-is-me-backend

# Remove image
docker rmi this-is-me-backend:latest
```

## 🔧 Maintenance

### Update Application
```bash
# 1. Pull latest code
git pull origin main

# 2. Rebuild image
./build.sh

# 3. Restart services
./restart.sh
```

### View Application Status
```bash
# Container status
docker compose -f docker-compose.prod.yml ps

# Container health
docker inspect --format='{{.State.Health.Status}}' this-is-me-backend

# Resource usage
docker stats this-is-me-backend
```

### Cleanup
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

## 🔍 Troubleshooting

### View Detailed Logs
```bash
# Last 100 lines
docker compose -f docker-compose.prod.yml logs --tail=100 backend

# Follow logs in real-time
docker compose -f docker-compose.prod.yml logs -f backend

# Logs for all services
./logs.sh
```

### Check Configuration
```bash
# View parsed docker-compose configuration
docker compose -f docker-compose.prod.yml config

# Validate docker-compose file
docker compose -f docker-compose.prod.yml config --quiet
```

### Restart Specific Service
```bash
docker compose -f docker-compose.prod.yml restart backend
docker compose -f docker-compose.prod.yml restart db
docker compose -f docker-compose.prod.yml restart redis
```

### Access Container Shell
```bash
# Backend container
docker compose -f docker-compose.prod.yml exec backend sh

# Database container
docker compose -f docker-compose.prod.yml exec db sh
```

### Run Django Management Commands
```bash
# Generic format
docker compose -f docker-compose.prod.yml exec backend python manage.py <command>

# Examples
docker compose -f docker-compose.prod.yml exec backend python manage.py check
docker compose -f docker-compose.prod.yml exec backend python manage.py showmigrations
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

## 📊 Monitoring

### Check Health Status
```bash
# Container health
docker inspect --format='{{.State.Health.Status}}' this-is-me-backend

# All containers status
docker compose -f docker-compose.prod.yml ps
```

### Resource Usage
```bash
# All containers
docker stats

# Specific container
docker stats this-is-me-backend

# Disk usage
docker system df
```

## 🔐 Security

### Update Dependencies
```bash
# 1. Update requirements.txt
# 2. Rebuild image
./build.sh

# 3. Restart services
./restart.sh
```

### Rotate Secrets
```bash
# 1. Update .env with new SECRET_KEY
# 2. Restart application
./restart.sh
```

## 📝 Environment Variables

### View Current Environment
```bash
docker compose -f docker-compose.prod.yml exec backend printenv | grep -E "ENV_NAME|DB_|REDIS_"
```

### Update Environment Variables
```bash
# 1. Edit .env file
nano .env

# 2. Restart services
./restart.sh
```

## 🚨 Emergency Procedures

### Stop Everything Immediately
```bash
docker compose -f docker-compose.prod.yml down
```

### Full Reset (⚠️ Destroys all data)
```bash
docker compose -f docker-compose.prod.yml down -v
rm -rf static/
./build.sh
./run.sh
```

### Recover from Failed Migration
```bash
./db-manage.sh shell
# In Django shell:
# from django.db import connection
# connection.cursor().execute("DELETE FROM django_migrations WHERE app='app_name' AND name='migration_name';")
# exit()
./db-manage.sh migrate
```

## 📚 Additional Resources

- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guide
- See [README.md](README.md) for project overview
- Docker Documentation: https://docs.docker.com/
- Django Documentation: https://docs.djangoproject.com/

