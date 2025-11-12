# External Services Configuration

This application requires external PostgreSQL and Redis services. This document provides guidance on setting them up.

## 🗄️ PostgreSQL Database

### Option 1: Local PostgreSQL

#### Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Docker (for development only):**
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_DB=this_is_me_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine
```

#### Create Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE this_is_me_db;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE this_is_me_db TO your_user;
\q
```

#### Configuration

Update your `.env`:
```env
DB_HOST=localhost
DB_NAME=this_is_me_db
DB_USER=your_user
DB_PASS=your_password
DB_PORT=5432
```

**For Docker on Linux**, use Docker's gateway IP:
```env
DB_HOST=172.17.0.1
```

**For Docker on Mac/Windows**, use special DNS:
```env
DB_HOST=host.docker.internal
```

### Option 2: Cloud PostgreSQL

#### AWS RDS

1. **Create RDS Instance**:
   - Go to AWS RDS Console
   - Create PostgreSQL database
   - Choose instance type
   - Configure VPC and security groups
   - Enable public accessibility (if needed)

2. **Security Group**:
   - Add inbound rule for PostgreSQL (port 5432)
   - Allow connections from your server's IP

3. **Configuration**:
```env
DB_HOST=your-db-instance.abc123.us-east-1.rds.amazonaws.com
DB_NAME=this_is_me_db
DB_USER=postgres
DB_PASS=your_secure_password
DB_PORT=5432
```

#### Google Cloud SQL

1. **Create Cloud SQL Instance**:
   - Go to Cloud SQL Console
   - Create PostgreSQL instance
   - Configure instance settings
   - Note the connection name

2. **Authorize Networks**:
   - Add your server's IP to authorized networks

3. **Configuration**:
```env
DB_HOST=your-cloud-sql-ip
DB_NAME=this_is_me_db
DB_USER=postgres
DB_PASS=your_secure_password
DB_PORT=5432
```

#### Azure Database for PostgreSQL

1. **Create Azure Database**:
   - Go to Azure Portal
   - Create PostgreSQL server
   - Configure firewall rules

2. **Configuration**:
```env
DB_HOST=your-server.postgres.database.azure.com
DB_NAME=this_is_me_db
DB_USER=your_user@your-server
DB_PASS=your_secure_password
DB_PORT=5432
```

#### DigitalOcean Managed Database

1. **Create Database Cluster**:
   - Go to DigitalOcean Control Panel
   - Create PostgreSQL cluster
   - Add your server's IP to trusted sources

2. **Configuration**:
```env
DB_HOST=your-db-cluster.db.ondigitalocean.com
DB_NAME=this_is_me_db
DB_USER=doadmin
DB_PASS=your_password
DB_PORT=25060
```

## 🔴 Redis Cache

### Option 1: Local Redis

#### Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Docker (for development only):**
```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine redis-server --requirepass your_redis_password
```

#### Configuration

Enable authentication in `/etc/redis/redis.conf`:
```
requirepass your_redis_password
```

Restart Redis:
```bash
sudo systemctl restart redis-server
```

Update your `.env`:
```env
USE_REDIS_CACHE=true
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_USE_SSL=false
```

**For Docker on Linux**:
```env
REDIS_HOST=172.17.0.1
```

**For Docker on Mac/Windows**:
```env
REDIS_HOST=host.docker.internal
```

### Option 2: Cloud Redis

#### AWS ElastiCache

1. **Create ElastiCache Cluster**:
   - Go to AWS ElastiCache Console
   - Create Redis cluster
   - Choose instance type
   - Enable encryption (optional)
   - Configure VPC and security groups

2. **Security Group**:
   - Add inbound rule for Redis (port 6379)
   - Allow connections from your server

3. **Configuration**:
```env
USE_REDIS_CACHE=true
REDIS_HOST=your-cluster.abc123.cache.amazonaws.com
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_USE_SSL=true
REDIS_VALIDATE_CERT=true
```

#### Redis Cloud (Redis Labs)

1. **Create Redis Instance**:
   - Sign up at redis.com
   - Create new database
   - Note endpoint and password

2. **Configuration**:
```env
USE_REDIS_CACHE=true
REDIS_HOST=your-endpoint.redis.cloud.redislabs.com
REDIS_PORT=12345
REDIS_PASSWORD=your_password
REDIS_USE_SSL=true
```

#### Azure Cache for Redis

1. **Create Redis Cache**:
   - Go to Azure Portal
   - Create Redis Cache
   - Configure settings

2. **Configuration**:
```env
USE_REDIS_CACHE=true
REDIS_HOST=your-cache.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=your_access_key
REDIS_USE_SSL=true
```

#### DigitalOcean Managed Redis

1. **Create Redis Cluster**:
   - Go to DigitalOcean Control Panel
   - Create Redis cluster
   - Add your server's IP to trusted sources

2. **Configuration**:
```env
USE_REDIS_CACHE=true
REDIS_HOST=your-redis-cluster.db.ondigitalocean.com
REDIS_PORT=25061
REDIS_PASSWORD=your_password
REDIS_USE_SSL=true
```

## 🔒 Security Best Practices

### PostgreSQL

1. **Use strong passwords**:
   - Minimum 16 characters
   - Mix of letters, numbers, and symbols

2. **Limit network access**:
   - Use firewall rules
   - Only allow specific IPs
   - Use VPC/private networks when possible

3. **Enable SSL/TLS**:
   - Configure PostgreSQL to require SSL connections
   - Use certificate validation

4. **Regular backups**:
   - Set up automated backups
   - Test restore procedures
   - Keep backups encrypted

### Redis

1. **Enable authentication**:
   - Always set a password
   - Use strong passwords

2. **Disable dangerous commands**:
   - Rename or disable FLUSHALL, FLUSHDB, CONFIG

3. **Use SSL/TLS**:
   - Enable SSL for production
   - Use certificate validation

4. **Network isolation**:
   - Bind to specific interfaces
   - Use firewall rules
   - Consider VPC/private networks

## 🧪 Testing Connections

### Test PostgreSQL Connection

From your server:
```bash
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
# Enter password when prompted
```

From Docker container:
```bash
cd deploy
docker compose -f docker-compose.prod.yml run --rm backend \
  python -c "from django.db import connection; connection.ensure_connection(); print('Database connected!')"
```

### Test Redis Connection

From your server:
```bash
redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD ping
# Should return: PONG
```

From Docker container:
```bash
cd deploy
docker compose -f docker-compose.prod.yml run --rm backend \
  python -c "import redis; r=redis.Redis(host='$REDIS_HOST', port=$REDIS_PORT, password='$REDIS_PASSWORD'); print(r.ping())"
# Should return: True
```

## 📊 Monitoring

### PostgreSQL

Monitor important metrics:
- Connection count
- Query performance
- Database size
- Replication lag (if applicable)

### Redis

Monitor important metrics:
- Memory usage
- Hit rate
- Connected clients
- Commands per second

## 🆘 Troubleshooting

### Cannot connect to PostgreSQL

1. **Check if PostgreSQL is running**:
   ```bash
   sudo systemctl status postgresql
   ```

2. **Check network connectivity**:
   ```bash
   telnet $DB_HOST 5432
   # or
   nc -zv $DB_HOST 5432
   ```

3. **Check PostgreSQL allows remote connections**:
   - Edit `postgresql.conf`: `listen_addresses = '*'`
   - Edit `pg_hba.conf`: Add appropriate connection rules

4. **Check firewall rules**:
   ```bash
   sudo ufw status
   sudo ufw allow 5432/tcp
   ```

### Cannot connect to Redis

1. **Check if Redis is running**:
   ```bash
   sudo systemctl status redis-server
   ```

2. **Check network connectivity**:
   ```bash
   telnet $REDIS_HOST 6379
   ```

3. **Check Redis allows remote connections**:
   - Edit `redis.conf`: `bind 0.0.0.0`
   - Restart Redis

4. **Check firewall rules**:
   ```bash
   sudo ufw allow 6379/tcp
   ```

### Docker networking issues

**For localhost services on Linux**:
```env
DB_HOST=172.17.0.1      # Docker bridge gateway
REDIS_HOST=172.17.0.1
```

**For localhost services on Mac/Windows**:
```env
DB_HOST=host.docker.internal
REDIS_HOST=host.docker.internal
```

**Alternative: Use host network mode** (already configured in docker-compose.prod.yml):
```yaml
network_mode: "host"
```

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [AWS RDS Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [Redis Security](https://redis.io/docs/management/security/)

