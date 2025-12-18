# Loan ETL Pipeline

โปรเจคนี้เป็น ETL (Extract, Transform, Load) pipeline สำหรับข้อมูล loan ที่จะสร้าง data warehouse 

## โครงสร้างโฟลเดอร์

```
pre-production/
├── config/
│   └── database.py        # การตั้งค่าฐานข้อมูลและพารามิเตอร์ต่างๆ
├── utils/
│   └── data_types.py      # ฟังก์ชันสำหรับวิเคราะห์ data types
├── etl/
│   ├── data_cleaning.py   # ฟังก์ชันทำความสะอาดข้อมูล
│   ├── dimensions.py      # ฟังก์ชันสร้าง dimension tables
│   ├── fact_table.py      # ฟังก์ชันสร้าง fact table
│   └── database_loader.py # ฟังก์ชันโหลดข้อมูลเข้า SQL Server
├── main.py               # ไฟล์หลักสำหรับรัน ETL process
└── README.md             # ไฟล์นี้
```

## วิธีใช้งาน

1. วางไฟล์ข้อมูล `LoanStats_web.csv` ไว้ที่ไหนก็ได้

2. แก้ไขการตั้งค่าใน `config/database.py`:
   - `FILE_CONFIG['input_file']` - แก้ path ให้ตรงกับที่วางไฟล์ไว้
   - `DB_CONFIG` - ข้อมูลการเชื่อมต่อฐานข้อมูล
   - `CLEANING_CONFIG` - พารามิเตอร์การทำความสะอาด

3. รันโปรแกรม:
   ```bash
   cd pre-production
   python main.py
   ```

## ขั้นตอนการทำงาน

1. **อ่านและวิเคราะห์ข้อมูล**: ตรวจสอบ data types ของแต่ละ column
2. **ทำความสะอาดข้อมูล**: 
   - ลบ columns ที่มี null มากเกิน 30%
   - แทนค่า null ใน emp_length ด้วย 'N/A'
   - กรอง application_type ที่เป็น '<NA>' ออก
   - แปลงรูปแบบวันที่และอัตราดอกเบี้ย
3. **สร้าง Dimension Tables**:
   - home_ownership_dim
   - loan_status_dim
   - issue_d_dim (พร้อม month และ year)
   - application_type_dim
   - emp_length_dim
4. **สร้าง Fact Table**: loans_fact พร้อม foreign keys และ measures
5. **โหลดเข้าฐานข้อมูล**: โหลดทั้ง dimensions และ fact table เข้า SQL Server

## ข้อกำหนดของระบบ

- Python 3.x
- pandas
- sqlalchemy
- pymssql
- re (built-in)

## หมายเหตุ

- โปรแกรมจะเก็บค่า null ไว้ใน columns เช่น annual_inc_joint, dti_joint เพื่อไม่ให้ค่าเฉลี่ยผิดเพี้ยน
- มีการตรวจสอบความถูกต้องของข้อมูลก่อนโหลดเข้าฐานข้อมูล
- ใช้ pymssql สำหรับเชื่อมต่อ SQL Server
