# Build stage
FROM python:3.8-slim as builder

# Install system dependencies for pymssql
RUN apt-get update && apt-get install -y \
    freetds-dev \
    freetds-bin \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Final stage
FROM python:3.8-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    freetds-bin \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL pipeline code
COPY pre-production/ ./pre-production/

# Create directory for data
RUN mkdir -p /app/data

# Environment variables (will be overridden at runtime)
ENV DB_SERVER=""
ENV DB_DATABASE="TestDB"
ENV DB_USERNAME="SA"
ENV DB_PASSWORD=""
ENV DATA_URL="https://storage.googleapis.com/26jun2023/LoanStats_web.csv"

# Add execution script
COPY deployment/run_etl.sh /app/
RUN chmod +x /app/run_etl.sh

# Default command
CMD ["/app/run_etl.sh"]
