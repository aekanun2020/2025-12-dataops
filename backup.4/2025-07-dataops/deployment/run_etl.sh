#!/bin/bash
set -e

echo "=== Starting ETL Pipeline ==="
echo "Time: $(date)"
echo "Environment: Production"

# Download data file
echo "Downloading data from: ${DATA_URL}"
curl -o /app/data/LoanStats_web.csv "${DATA_URL}"

# Update database config
cat > /app/pre-production/config/database.py << EOF
"""
การตั้งค่าฐานข้อมูล
ไฟล์นี้เก็บค่า configuration สำหรับการเชื่อมต่อ database
"""

# ค่าการเชื่อมต่อ SQL Server
DB_CONFIG = {
    'server': '${DB_SERVER}',
    'database': '${DB_DATABASE}',
    'username': '${DB_USERNAME}',
    'password': '${DB_PASSWORD}'
}

# ตั้งค่าสำหรับการอ่านไฟล์
FILE_CONFIG = {
    'input_file': '/app/data/LoanStats_web.csv',
    'delimiter': ',',
    'has_headers': True
}

# ตั้งค่าสำหรับการทำ data cleaning
CLEANING_CONFIG = {
    'max_null_percentage': 30,  # ลบ column ที่มี null เกิน 30%
    'acceptable_max_null': 26    # จำนวน null ที่ยอมรับได้ในแต่ละ column
}
EOF

# Run ETL
echo "Running ETL pipeline..."
cd /app/pre-production
python main.py

echo "=== ETL Pipeline Completed ==="
echo "End time: $(date)"
