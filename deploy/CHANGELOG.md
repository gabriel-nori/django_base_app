# Deployment Configuration Changelog

## External Services Configuration (Latest)

### Changes Made

#### Docker Compose (`docker-compose.prod.yml`)
- ✅ **Removed** PostgreSQL container (now external)
- ✅ **Removed** Redis container (now external)
- ✅ **Removed** internal Docker networks
- ✅ **Added** `network_mode: "host"` for accessing external services
- ✅ **Updated** environment variables to use `${DB_HOST}` and `${REDIS_HOST}`
- ✅ **Removed** service dependencies on `db` and `redis`
- ✅ Only contains the `backend` service

#### Environment Configuration (`env.prod.example`)
- ✅ **Updated** `DB_HOST` to point to external PostgreSQL
- ✅ **Updated** `REDIS_HOST` to point to external Redis
- ✅ **Added** comments for external service configuration
- ✅ **Added** examples for localhost and cloud providers

#### Documentation
- ✅ **Created** `EXTERNAL_SERVICES.md` with comprehensive setup guides:
  - Local PostgreSQL and Redis installation
  - Cloud provider configurations (AWS, GCP, Azure, DigitalOcean)
  - Security best practices
  - Connection testing procedures
  - Troubleshooting guides

- ✅ **Updated** `PRODUCTION_SETUP.md`:
  - Added Step 0 for external services setup
  - Updated prerequisites
  - Added references to external services documentation

- ✅ **Updated** `DEPLOYMENT.md`:
  - Added prerequisites for external services
  - Updated configuration examples
  - Added external services section

- ✅ **Updated** `README.md`:
  - Added external services to checklist
  - Updated references

### Migration Guide

If you were using the previous configuration with Docker PostgreSQL and Redis:

#### Option 1: Migrate to External Services

1. **Backup your data** from the Docker containers:
   ```bash
   # Backup PostgreSQL
   docker compose -f docker-compose.prod.yml exec db \
     pg_dump -U postgres your_db > backup.sql
   
   # Backup Redis (if needed)
   docker compose -f docker-compose.prod.yml exec redis \
     redis-cli save
   docker cp this-is-me-redis:/data/dump.rdb ./redis-backup.rdb
   ```

2. **Set up external PostgreSQL and Redis** (see `EXTERNAL_SERVICES.md`)

3. **Restore your data** to the new external services

4. **Update `.env`** with new `DB_HOST` and `REDIS_HOST`

5. **Rebuild and restart**:
   ```bash
   cd deploy
   ./build.sh
   ./run.sh
   ```

#### Option 2: Continue Using Docker Services (Not Recommended)

If you need to keep using Docker containers for PostgreSQL and Redis, you can:

1. Create a separate `docker-compose.services.yml`:
   ```yaml
   version: '3.8'
   
   services:
     db:
       image: postgres:15-alpine
       container_name: this-is-me-db
       restart: unless-stopped
       environment:
         POSTGRES_DB: ${DB_NAME}
         POSTGRES_USER: ${DB_USER}
         POSTGRES_PASSWORD: ${DB_PASS}
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
     
     redis:
       image: redis:7-alpine
       container_name: this-is-me-redis
       restart: unless-stopped
       command: redis-server --requirepass ${REDIS_PASSWORD}
       volumes:
         - redis_data:/data
       ports:
         - "6379:6379"
   
   volumes:
     postgres_data:
     redis_data:
   ```

2. Run services separately:
   ```bash
   docker compose -f docker-compose.services.yml up -d
   ```

3. Configure `.env` to use localhost:
   ```env
   DB_HOST=172.17.0.1      # Linux
   # or
   DB_HOST=host.docker.internal  # Mac/Windows
   
   REDIS_HOST=172.17.0.1   # Linux
   # or
   REDIS_HOST=host.docker.internal  # Mac/Windows
   ```

### Benefits of External Services

1. **Scalability**: Easier to scale database and cache independently
2. **Management**: Use managed services (RDS, ElastiCache, etc.)
3. **Backup**: Better backup and disaster recovery options
4. **Performance**: Dedicated resources for database and cache
5. **Monitoring**: Better monitoring and observability
6. **Flexibility**: Easy to switch providers or configurations

### Network Configuration

The application now uses `network_mode: "host"` which means:

- ✅ Container can access all services on the host
- ✅ No port mapping needed for external services
- ✅ Simpler networking configuration
- ⚠️  Container shares host's network namespace
- ⚠️  PORT environment variable is still used for the application

### Environment Variables Reference

Required variables for external services:

```env
# PostgreSQL (External)
DB_HOST=your-postgres-host      # Required
DB_NAME=this_is_me_db           # Required
DB_USER=postgres                # Required
DB_PASS=your_password           # Required
DB_PORT=5432                    # Optional (default: 5432)

# Redis (External)
REDIS_HOST=your-redis-host      # Required if USE_REDIS_CACHE=true
REDIS_PORT=6379                 # Optional (default: 6379)
REDIS_PASSWORD=your_password    # Required if Redis has auth
USE_REDIS_CACHE=true            # Optional (default: true)
REDIS_DB_INDEX=1                # Optional (default: 1)
REDIS_USE_SSL=false             # Optional (default: false)
```

### Testing the Configuration

After updating:

1. **Test database connection**:
   ```bash
   cd deploy
   docker compose -f docker-compose.prod.yml run --rm backend \
     python manage.py check --database default
   ```

2. **Test Redis connection** (if enabled):
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend \
     python -c "from django.core.cache import cache; cache.set('test', 'ok'); print(cache.get('test'))"
   ```

3. **View startup logs**:
   ```bash
   ./logs.sh backend
   ```

### Troubleshooting

See [EXTERNAL_SERVICES.md](EXTERNAL_SERVICES.md) for detailed troubleshooting guides.

Common issues:
- Connection refused: Check if services are running and accessible
- Authentication failed: Verify passwords in `.env`
- Host not found: Verify hostnames/IPs are correct
- Timeout: Check firewall rules and network connectivity

### Support

For questions or issues:
- Review `EXTERNAL_SERVICES.md` for setup guides
- Check `DEPLOYMENT.md` for deployment procedures
- See `COMMANDS.md` for available commands

