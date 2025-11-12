# Production Setup - Quick Start Guide

This document provides a streamlined guide to get your This Is Me Backend running in production.

## ✅ What's Been Set Up

Your project now includes:

1. **Production-Ready Dockerfile**
   - Multi-stage build for smaller image size
   - Non-root user for security
   - Optimized Gunicorn configuration
   - Health checks

2. **Docker Compose Configuration**
   - PostgreSQL database
   - Redis cache
   - Automatic migrations on startup
   - Network isolation

3. **Management Scripts**
   - `build.sh` - Build the Docker image
   - `run.sh` - Start all services
   - `stop.sh` - Stop all services
   - `restart.sh` - Restart services
   - `logs.sh` - View application logs
   - `db-manage.sh` - Database management utilities

4. **Documentation**
   - `DEPLOYMENT.md` - Comprehensive deployment guide
   - `EXTERNAL_SERVICES.md` - PostgreSQL & Redis setup guide
   - `COMMANDS.md` - Command reference
   - `env.prod.example` - Environment configuration template

## 🚀 Get Started in 4 Steps

### Step 0: Set Up External Services (IMPORTANT!)

**Before deploying, you need external PostgreSQL and Redis services.**

See detailed setup guide: [EXTERNAL_SERVICES.md](EXTERNAL_SERVICES.md)

Quick options:
- **Local**: Install PostgreSQL and Redis on your server
- **Cloud**: Use AWS RDS/ElastiCache, Google Cloud SQL, Azure, etc.
- **Docker** (dev only): Run separate PostgreSQL and Redis containers

### Step 1: Configure Environment

```bash
cd deploy
cp env.prod.example .env
```

Edit `.env` and set these **required** variables:
- `SECRET_KEY` - Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `DB_HOST` - Your external PostgreSQL host (e.g., `localhost`, `your-db.example.com`, AWS RDS endpoint)
- `DB_NAME` - Your database name (e.g., `this_is_me_db`)
- `DB_USER` - Database user (e.g., `postgres`)
- `DB_PASS` - Strong database password
- `REDIS_HOST` - Your external Redis host (e.g., `localhost`, `your-redis.example.com`, AWS ElastiCache endpoint)
- `REDIS_PASSWORD` - Redis password (if authentication is enabled)
- `ALLOWED_HOSTS` - Your domains (e.g., `yourdomain.com,api.yourdomain.com`)

### Step 2: Build

```bash
./build.sh
```

This will:
- Validate your environment configuration
- Build the production Docker image
- Install all dependencies

### Step 3: Run

```bash
./run.sh
```

This will:
- Start PostgreSQL and Redis
- Run database migrations
- Initialize application objects
- Start the backend API

Your API will be available at `http://localhost:8000`

## 📋 Common Operations

All commands must be run from the `deploy` folder:

```bash
cd deploy

# View logs
./logs.sh backend

# Stop application
./stop.sh

# Restart after code changes
./build.sh && ./restart.sh

# Create admin user
./db-manage.sh createsuperuser

# Backup database
./db-manage.sh backup

# Run migrations
./db-manage.sh migrate
```

## 🔍 Verify Installation

After running, verify everything is working:

```bash
# Check container status
docker compose -f docker-compose.prod.yml ps

# Check backend logs
./logs.sh backend

# Test API (replace with actual endpoint)
curl http://localhost:8000/api/
```

Expected output:
- All containers show "Up" status
- No error messages in logs
- API responds successfully

## 🛠️ Troubleshooting

### Services won't start
```bash
# Check logs for errors
./logs.sh

# Verify environment variables
cat .env | grep -v "^#"

# Rebuild from scratch
./stop.sh
./build.sh
./run.sh
```

### Database connection errors
```bash
# Check database logs
./logs.sh db

# Verify database is running
docker compose -f docker-compose.prod.yml ps db

# Check environment variables
docker compose -f docker-compose.prod.yml exec backend env | grep DB_
```

### Port already in use
Edit `.env` and change:
```
PORT=8001  # or another available port
```
Then restart: `./restart.sh`

## 📚 Next Steps

1. **Configure Production Domain**
   - Update `ALLOWED_HOSTS` in `.env`
   - Set up reverse proxy (Nginx/Traefik)
   - Configure SSL/TLS certificates

2. **Set Up Monitoring**
   - Configure logging aggregation
   - Set up health check monitoring
   - Configure alerting

3. **Configure Backups**
   - Schedule regular database backups
   - Set up backup retention policy
   - Test backup restoration

4. **Security Hardening**
   - Review security settings
   - Set up firewall rules
   - Configure rate limiting
   - Enable HTTPS only

## 🆘 Getting Help

- **Detailed Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Command Reference**: See [COMMANDS.md](COMMANDS.md)
- **Project Documentation**: See [README.md](README.md)

## 📝 Architecture Overview

```
┌─────────────────────────────────────────┐
│         Nginx/Reverse Proxy             │
│         (SSL Termination)               │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      This Is Me Backend                 │
│      (Docker Container)                 │
│      Gunicorn + Django                  │
│      Port: 8000                         │
└────┬─────────────────────┬──────────────┘
     │                     │
┌────▼──────────┐   ┌──────▼───────┐
│  PostgreSQL   │   │    Redis     │
│  (External)   │   │  (External)  │
└───────────────┘   └──────────────┘
```

## 🔐 Security Checklist

- [ ] Secret key is randomly generated
- [ ] Database password is strong (16+ characters)
- [ ] Redis password is set
- [ ] ALLOWED_HOSTS is configured correctly
- [ ] ENV_NAME is set to "PROD"
- [ ] Debug mode is disabled (ENV_NAME != "DEV")
- [ ] SSL/TLS is configured
- [ ] Firewall rules are in place
- [ ] Backups are configured
- [ ] Monitoring is set up

## 🎉 You're Ready!

Your production environment is now configured and ready to serve traffic. Remember to:

1. Keep your `.env` file secure (never commit to git)
2. Regularly update dependencies
3. Monitor logs and performance
4. Back up your database regularly
5. Test disaster recovery procedures

For more detailed information, see the complete [DEPLOYMENT.md](DEPLOYMENT.md) guide.

