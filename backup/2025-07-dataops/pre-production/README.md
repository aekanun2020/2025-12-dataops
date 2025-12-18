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

## การรัน Unit Tests

### เป้าหมายของการทดสอบ

Unit Testing ในโปรเจคนี้มีเป้าหมายเพื่อ**ประเมินความถูกต้องของข้อมูล** ไม่ใช่เพื่อประเมิน code quality:
- ข้อมูลที่ผ่านการ transform ถูกต้องตามที่คาดหวัง
- จำนวนข้อมูลหลังการประมวลผลถูกต้อง
- รูปแบบข้อมูล (data types, formats) ถูกแปลงอย่างถูกต้อง

### คำสั่งทดสอบ

**รันทั้งหมดพร้อม coverage:**
```bash
./run_all_tests.sh
```

**รันทั้งหมดแบบธรรมดา:**
```bash
pytest tests/ -v
```

**รันเฉพาะ test_data_cleaning** - ทดสอบการทำความสะอาดข้อมูล:
```bash
pytest tests/test_data_cleaning.py -v
```
| Test Case | ตรวจสอบอะไร |
|-----------|-------------|
| test_emp_length_null_replacement | Null values ใน emp_length ถูกแทนที่ด้วย 'N/A' |
| test_application_type_na_filter | ข้อมูล `<NA>` ถูกกรองออก |
| test_issue_d_datetime_conversion | Date formats ถูกแปลงเป็น datetime |
| test_int_rate_percentage_conversion | Percentage strings ถูกแปลงเป็นตัวเลขทศนิยม |
| test_data_integrity_after_cleaning | ข้อมูลอื่นยังคงถูกต้องหลัง clean |

**รันเฉพาะ test_data_quality** - ทดสอบความถูกต้องของ Star Schema:
```bash
pytest tests/test_data_quality.py -v
```
| Test Case | ตรวจสอบอะไร |
|-----------|-------------|
| test_dimension_unique_values | Dimension tables ไม่มี duplicate |
| test_fact_foreign_keys_exist | ทุก FK ใน fact table มีอยู่ใน dimension |
| test_loan_amount_positive | loan_amnt, funded_amnt, installment เป็นค่าบวก |
| test_funded_amount_not_exceed_loan | funded_amnt ไม่เกิน loan_amnt |
| test_interest_rate_range | interest rate อยู่ในช่วง 0-1 |

**รันพร้อม HTML coverage report:**
```bash
pytest tests/ -v --cov=pre-production/etl --cov-report=html
```
Report จะอยู่ที่ `htmlcov/index.html`

## หมายเหตุ

- โปรแกรมจะเก็บค่า null ไว้ใน columns เช่น annual_inc_joint, dti_joint เพื่อไม่ให้ค่าเฉลี่ยผิดเพี้ยน
- มีการตรวจสอบความถูกต้องของข้อมูลก่อนโหลดเข้าฐานข้อมูล
- ใช้ pymssql สำหรับเชื่อมต่อ SQL Server
