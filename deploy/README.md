# Deploy Folder

This folder contains all deployment-related files and scripts for the This Is Me Backend application.

## 📁 Contents

### Scripts (Executable)
- **`build.sh`** - Build the Docker image
- **`run.sh`** - Start all services
- **`stop.sh`** - Stop all services
- **`restart.sh`** - Restart services
- **`logs.sh`** - View application logs
- **`db-manage.sh`** - Database management utilities

### Configuration Files
- **`dockerfile`** - Multi-stage production Dockerfile
- **`docker-compose.prod.yml`** - Docker Compose configuration
- **`.dockerignore`** - Docker build context exclusions
- **`env.prod.example`** - Environment variables template

### Documentation
- **`PRODUCTION_SETUP.md`** - Quick start guide (⭐ START HERE)
- **`DEPLOYMENT.md`** - Comprehensive deployment guide
- **`EXTERNAL_SERVICES.md`** - PostgreSQL & Redis setup guide
- **`COMMANDS.md`** - Complete command reference

## 🚀 Quick Start

### 1. Configure Environment
```bash
cd deploy
cp env.prod.example .env
# Edit .env with your production settings
```

### 2. Build
```bash
./build.sh
```

### 3. Run
```bash
./run.sh
```

## 📝 Important Notes

- **All commands must be run from the `deploy` folder**
- The `.env` file must be in the `deploy` folder
- Docker build context is the parent directory
- Scripts reference files relative to the deploy folder

## 📚 Documentation

For detailed instructions, see:
- **Getting Started**: [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)
- **Full Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Commands**: [COMMANDS.md](COMMANDS.md)

## 🔧 Usage Examples

```bash
# Navigate to deploy folder
cd deploy

# Configure environment
cp env.prod.example .env
nano .env

# Build and run
./build.sh
./run.sh

# View logs
./logs.sh backend

# Manage database
./db-manage.sh migrate
./db-manage.sh createsuperuser
./db-manage.sh backup

# Stop services
./stop.sh
```

## 📂 File Structure

```
deploy/
├── build.sh                  # Build script
├── run.sh                    # Run script
├── stop.sh                   # Stop script
├── restart.sh                # Restart script
├── logs.sh                   # Logs viewer
├── db-manage.sh              # Database utilities
├── dockerfile                # Docker configuration
├── docker-compose.prod.yml   # Compose configuration
├── .dockerignore             # Build exclusions
├── env.prod.example          # Environment template
├── .env                      # Your environment (create this)
├── PRODUCTION_SETUP.md       # Quick start guide
├── DEPLOYMENT.md             # Deployment guide
├── COMMANDS.md               # Command reference
└── README.md                 # This file
```

## ⚠️ Before Deploying

- [ ] **Set up external PostgreSQL database** (see [EXTERNAL_SERVICES.md](EXTERNAL_SERVICES.md))
- [ ] **Set up external Redis server** (see [EXTERNAL_SERVICES.md](EXTERNAL_SERVICES.md))
- [ ] Copy `env.prod.example` to `.env`
- [ ] Update all required environment variables
- [ ] Generate a secure `SECRET_KEY`
- [ ] Set strong passwords for database and Redis
- [ ] Configure `ALLOWED_HOSTS` correctly
- [ ] Configure `DB_HOST` and `REDIS_HOST` to point to your external services
- [ ] Ensure Docker and Docker Compose are installed

## 🆘 Need Help?

1. **Quick Start**: See [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)
2. **Detailed Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Command Reference**: See [COMMANDS.md](COMMANDS.md)
4. **Project Overview**: See [../README.md](../README.md)

