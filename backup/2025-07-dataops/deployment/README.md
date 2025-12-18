# Deployment Configuration

This directory contains all files needed for Continuous Deployment (CD) of the Loan ETL Pipeline.

## Files

### Dockerfile
Builds the ETL pipeline container with:
- Python 3.8 base image
- Required dependencies (pandas, sqlalchemy, pymssql)
- ETL scripts from pre-production/
- Runtime configuration via environment variables

### run_etl.sh
Script that runs inside the container to:
- Download data from Google Cloud Storage
- Update database configuration
- Execute the ETL pipeline

### docker-compose.yml
For local testing and development:
```bash
# Test locally (set DB_PASSWORD first)
export DB_PASSWORD="your-password"
docker-compose up --build
```

### deploy.sh
Deployment script used by CI/CD to:
- Pull latest image from Docker Hub
- Stop old container
- Start new container
- Setup daily cron job (14:30 Bangkok time)

## Environment Variables

Required environment variables:
- `DB_SERVER`: SQL Server address (default: 34.16.100.219)
- `DB_DATABASE`: Database name (default: TestDB)
- `DB_USERNAME`: Database user (default: SA)
- `DB_PASSWORD`: Database password (required)
- `DATA_URL`: Source data URL (default: Google Cloud Storage URL)

## Deployment Flow

1. CI tests pass
2. Build Docker image
3. Push to `thaibigdata/dataops-pipeline:latest`
4. Run `deploy.sh` on production host
5. Container runs immediately and then daily at 14:30

## Manual Deployment

```bash
# Set database password
export DB_PASSWORD="your-password"

# Run deployment
./deploy.sh
```

## Monitoring

Check logs:
```bash
# Container logs
docker logs loan-etl-pipeline

# Cron logs
tail -f /var/log/loan-etl/cron.log
```

Check container status:
```bash
docker ps -f name=loan-etl-pipeline
```
