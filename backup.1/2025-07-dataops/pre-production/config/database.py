"""
การตั้งค่าฐานข้อมูล
ไฟล์นี้เก็บค่า configuration สำหรับการเชื่อมต่อ database
"""

# ค่าการเชื่อมต่อ SQL Server
DB_CONFIG = {
    'server': '34.68.42.255',
    'database': 'TestDB',
    'username': 'sa',
    'password': 'Passw0rd123456'
}

# ตั้งค่าสำหรับการอ่านไฟล์
FILE_CONFIG = {
    'input_file': '/Users/grizzlymacbookpro/Desktop/test/2025-12-18/LoanStats_web.csv',
    'delimiter': ',',
    'has_headers': True
}

# ตั้งค่าสำหรับการทำ data cleaning
CLEANING_CONFIG = {
    'max_null_percentage': 30,  # ลบ column ที่มี null เกิน 30%
    'acceptable_max_null': 26    # จำนวน null ที่ยอมรับได้ในแต่ละ column
}
