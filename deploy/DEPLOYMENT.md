# This Is Me Backend - Production Deployment Guide

This guide covers deploying the This Is Me Backend API in production using Docker.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose V2 or docker-compose 1.29+
- 2GB+ RAM
- **External PostgreSQL database** (v12+, required)
- **External Redis server** (v6+, optional but recommended)

## 🚀 Quick Start

All deployment files are located in the `deploy` folder.

### 0. Set Up External Services

**Prerequisites**: Before deploying, you must have:
- A PostgreSQL database (v12+) accessible from your server
- A Redis server (v6+) accessible from your server

📖 **See [EXTERNAL_SERVICES.md](EXTERNAL_SERVICES.md) for detailed setup instructions**

### 1. Environment Configuration

Navigate to the deploy folder and copy the example environment file:

```bash
cd deploy
cp env.prod.example .env
```

Edit `.env` and set the following required variables:

- `SECRET_KEY`: Django secret key (generate a secure random string)
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASS`: PostgreSQL password
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (e.g., `yourdomain.com,api.yourdomain.com`)

### 2. Build the Application

From the `deploy` folder:

```bash
./build.sh
```

This will:
- Validate your environment configuration
- Build the Docker image with all dependencies
- Create a production-ready container

### 3. Run the Application

From the `deploy` folder:

```bash
./run.sh
```

This will:
- Connect to your external PostgreSQL database
- Connect to your external Redis server (if enabled)
- Run database migrations
- Initialize default objects
- Start the backend API with Gunicorn

The API will be available at `http://localhost:8000` (or the port specified in `.env`)

## 🛠️ Management Scripts

All scripts are located in the root directory:

### Build
```bash
./build.sh          # Build the Docker image
```

### Run & Stop
```bash
./run.sh            # Start all services
./stop.sh           # Stop all services
./restart.sh        # Restart all services
```

### Logs
```bash
./logs.sh           # View logs for all services
./logs.sh backend   # View logs for backend only
./logs.sh db        # View logs for database only
```

## 🐳 Docker Commands

### Using Docker Compose Directly

```bash
# Start services in background
docker compose -f docker-compose.prod.yml up -d

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Stop services
docker compose -f docker-compose.prod.yml down

# Rebuild and restart
docker compose -f docker-compose.prod.yml up -d --build

# View running containers
docker compose -f docker-compose.prod.yml ps
```

### Using Docker Directly

```bash
# Build image
docker build -t this-is-me-backend:latest -f dockerfile .

# Run container (requires database setup)
docker run -d \
  --name this-is-me-backend \
  --env-file .env \
  -p 8000:8000 \
  this-is-me-backend:latest
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENV_NAME` | Environment name | `PROD` | No |
| `SECRET_KEY` | Django secret key | - | Yes |
| `DB_NAME` | Database name | - | Yes |
| `DB_USER` | Database user | - | Yes |
| `DB_PASS` | Database password | - | Yes |
| `DB_HOST` | Database host (external) | - | Yes |
| `REDIS_HOST` | Redis host (external) | - | No |
| `REDIS_PASSWORD` | Redis password | `changeme` | No |
| `USE_REDIS_CACHE` | Enable Redis caching | `true` | No |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | - | Yes |
| `PORT` | Application port | `8000` | No |
| `APP_NAME` | Application name | `This Is Me` | No |
| `LOG_LEVEL` | Logging level | `info` | No |

### Gunicorn Configuration

The application runs with the following Gunicorn settings:

- **Workers**: 4 (adjust based on CPU cores: 2-4 × cores)
- **Threads**: 2 per worker
- **Worker Class**: gthread (threaded workers)
- **Timeout**: 120 seconds
- **Graceful Timeout**: 30 seconds

To customize, edit the `CMD` in `dockerfile` or override in `docker-compose.prod.yml`.

## 🔒 Security Best Practices

1. **Secret Key**: Generate a secure random key:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Database Password**: Use strong passwords (minimum 16 characters)

3. **Allowed Hosts**: Only include domains you control

4. **Non-root User**: The container runs as a non-root user (`appuser`)

5. **Environment Variables**: Never commit `.env` to version control

6. **HTTPS**: Use a reverse proxy (Nginx/Traefik) with SSL/TLS in production

## 📊 Monitoring & Health Checks

### Health Check Endpoint

The container includes a health check that monitors:
- Application availability
- Response time

Access it at: `http://localhost:8000/api/health/`

### Container Health Status

```bash
docker inspect --format='{{.State.Health.Status}}' this-is-me-backend
```

### Logs

```bash
# Real-time logs
./logs.sh backend

# Last 100 lines
docker compose -f docker-compose.prod.yml logs --tail=100 backend
```

## 🔄 Database Migrations

Migrations run automatically on container start. To run manually:

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

## 🧹 Cleanup

### Remove all containers and volumes
```bash
docker compose -f docker-compose.prod.yml down -v
```

### Remove Docker images
```bash
docker rmi this-is-me-backend:latest
```

## 🌐 Reverse Proxy Setup (Nginx Example)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static/;
    }
}
```

## 📝 Troubleshooting

### Container won't start
1. Check logs: `./logs.sh backend`
2. Verify environment variables: `docker compose -f docker-compose.prod.yml config`
3. Check database connectivity: `docker compose -f docker-compose.prod.yml exec backend python manage.py check`

### Database connection errors
1. Ensure database is running: `docker compose -f docker-compose.prod.yml ps db`
2. Verify credentials in `.env`
3. Check database logs: `./logs.sh db`

### Static files not loading
1. Rebuild image: `./build.sh`
2. Check static files: `docker compose -f docker-compose.prod.yml exec backend ls -la /backend/static`

## 🔧 Advanced Configuration

### Custom Gunicorn Settings

Edit `docker-compose.prod.yml` command section:

```yaml
command: >
  sh -c "python manage.py migrate --noinput &&
         gunicorn config.wsgi:application
         --bind 0.0.0.0:8000
         --workers 8
         --threads 4
         --timeout 180"
```

### External Database and Redis Configuration

The Docker Compose setup is already configured to use external PostgreSQL and Redis services.

**For local external services:**
```env
DB_HOST=localhost
REDIS_HOST=localhost
```

**For cloud services (AWS RDS, ElastiCache, etc.):**
```env
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
REDIS_HOST=your-elasticache-endpoint.region.cache.amazonaws.com
```

**Important**: Ensure your external services allow connections from your Docker container:
- For localhost: Use `host.docker.internal` on Mac/Windows, or `172.17.0.1` on Linux
- For cloud services: Configure security groups/firewall rules appropriately

### Persistent Data

Volumes are automatically created for:
- Static files: `static_volume`

**Note**: PostgreSQL and Redis data are managed externally on your database/cache servers.

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 💡 Support

For issues or questions, please check the project repository or contact the development team.

