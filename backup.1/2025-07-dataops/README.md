# Loan ETL Pipeline with CI/CD

โปรเจคนี้เป็น ETL (Extract, Transform, Load) pipeline สำหรับข้อมูล loan พร้อมระบบ CI/CD

## โครงสร้างโปรเจค

```
2025-07-dataops/
├── pre-production/        # Source code หลัก (ดู README ใน folder)
├── tests/                 # Unit tests
├── .github/               # GitHub Actions CI
├── Jenkinsfile            # Jenkins CI configuration
├── requirements.txt       # Python dependencies  
├── pytest.ini             # Pytest configuration
├── run_all_tests.sh       # Script รัน test suite ทั้งหมด
└── README.md              # ไฟล์นี้
```

## เอกสารประกอบ

- [วิธีใช้งาน ETL Pipeline](./pre-production/README.md) - การตั้งค่า, การรัน, ขั้นตอนการทำงาน

## การติดตั้ง

1. Clone repository:
```bash
git clone <repository-url>
cd 2025-07-dataops
```

2. สร้าง virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

---

## เป้าหมายของการทดสอบ (Testing Goal)

**สำคัญ:** การทำ Unit Testing ในโปรเจคนี้ **ไม่ได้** มีเป้าหมายเพื่อประเมิน code quality แต่มีเป้าหมายเพื่อ:

**ประเมินความถูกต้องของข้อมูลที่ function คายออกมา**
- ตรวจสอบว่า **ข้อมูลที่ผ่านการ transform** มีความถูกต้องตามที่คาดหวัง
- ตรวจสอบว่า **จำนวนข้อมูล** หลังการประมวลผลถูกต้อง
- ตรวจสอบว่า **รูปแบบข้อมูล** (data types, formats) ถูกแปลงอย่างถูกต้อง

**ตัวอย่างสิ่งที่ทดสอบ:**
- Null values ถูกแทนที่ด้วยค่าที่เหมาะสมหรือไม่
- ข้อมูลที่ไม่ต้องการถูกกรองออกถูกต้องหรือไม่  
- Date formats ถูกแปลงเป็น datetime objects หรือไม่
- Percentage strings ถูกแปลงเป็นตัวเลขทศนิยมหรือไม่

**สิ่งที่ไม่ได้ทดสอบ:**
- Code quality หรือ coding standards
- Performance หรือ optimization
- Code coverage เพื่อความสมบูรณ์ของ test cases

เป้าหมายหลักคือ **ให้มั่นใจว่าข้อมูลที่ได้จาก ETL pipeline มีความถูกต้องและพร้อมใช้งาน**

---

## การรัน Unit Tests

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

---

## CI/CD Pipeline

### GitHub Actions
- **Trigger**: Push to main/develop หรือ Pull Request
- **Test Matrix**: Python 3.8, 3.9, 3.10
- **Features**: Unit testing, Test reports, Coverage reports, Artifact upload

### Jenkins
- **Features**: Docker container, Unit testing with HTML reports, Coverage reports, Test results archiving

**การตั้งค่า Jenkins:**
1. สร้าง Pipeline job ใหม่
2. เลือก "Pipeline script from SCM"
3. ระบุ Git repository URL
4. Script path: `Jenkinsfile`

---

## ข้อกำหนดระบบ

- Python 3.8+
- SQL Server (สำหรับรัน ETL จริง - ไม่จำเป็นสำหรับรัน tests)
- Docker (สำหรับ Jenkins CI)
- Git
