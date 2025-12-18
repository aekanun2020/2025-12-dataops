# Loan ETL Pipeline with CI/CD

โปรเจคนี้เป็น ETL (Extract, Transform, Load) pipeline สำหรับข้อมูล loan พร้อมระบบ CI/CD

## 🎯 เป้าหมายของการทดสอบ (Testing Goal)

**สำคัญ:** การทำ Unit Testing ในโปรเจคนี้ **ไม่ได้** มีเป้าหมายเพื่อประเมิน code quality แต่มีเป้าหมายเพื่อ:

### ✅ ประเมินความถูกต้องของข้อมูลที่ function คายออกมา

- ตรวจสอบว่า **ข้อมูลที่ผ่านการ transform** มีความถูกต้องตามที่คาดหวัง
- ตรวจสอบว่า **จำนวนข้อมูล** หลังการประมวลผลถูกต้อง
- ตรวจสอบว่า **รูปแบบข้อมูล** (data types, formats) ถูกแปลงอย่างถูกต้อง

### 📊 ตัวอย่างการทดสอบ:
1. **Null values** ถูกแทนที่ด้วยค่าที่เหมาะสมหรือไม่
2. **ข้อมูลที่ไม่ต้องการ** ถูกกรองออกถูกต้องหรือไม่  
3. **Date formats** ถูกแปลงเป็น datetime objects หรือไม่
4. **Percentage strings** ถูกแปลงเป็นตัวเลขทศนิยมหรือไม่

### ❌ สิ่งที่เราไม่ได้ทดสอบ:
- Code quality หรือ coding standards
- Performance หรือ optimization
- Code coverage เพื่อความสมบูรณ์ของ test cases

เป้าหมายหลักคือ **ให้มั่นใจว่าข้อมูลที่ได้จาก ETL pipeline มีความถูกต้องและพร้อมใช้งาน**

## โครงสร้างโปรเจค

```
2025-07-25/
├── pre-production/         # Source code หลัก
│   ├── config/            # Configuration files
│   ├── utils/             # Utility functions
│   ├── etl/               # ETL functions
│   └── main.py            # Main ETL script
│
├── tests/                 # Unit tests
│   ├── test_data_cleaning.py      # Data transformation tests
│   ├── test_data_quality.py       # Data quality tests
│   └── fixtures/          # Test data
│
├── .github/               # GitHub Actions CI
│   └── workflows/
│       └── ci.yml
│
├── Jenkinsfile           # Jenkins CI configuration
├── requirements.txt      # Python dependencies  
├── pytest.ini           # Pytest configuration
├── run_all_tests.sh     # Script รัน test suite ทั้งหมด
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## การติดตั้ง

1. Clone repository:
```bash
git clone <repository-url>
cd 2025-07-25
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

## การรัน ETL Pipeline

```bash
cd pre-production
python main.py
```

## การรัน Unit Tests

### รันทั้งหมดด้วย script:
```bash
./run_all_tests.sh
```

### รันทั้งหมด:
```bash
pytest tests/ -v
```

### รันเฉพาะ test_data_cleaning:
```bash
pytest tests/test_data_cleaning.py -v
```

### รันเฉพาะ test_data_quality:
```bash
pytest tests/test_data_quality.py -v
```

### รันพร้อม coverage report:
```bash
pytest tests/ -v --cov=pre-production/etl --cov-report=html
```

## CI/CD Pipeline

### GitHub Actions
- **Trigger**: Push to main/develop หรือ Pull Request
- **Test Matrix**: Python 3.8, 3.9, 3.10
- **Features**:
  - Unit testing with pytest
  - Test reports และ coverage reports
  - Artifact upload

### Jenkins
- **Features**:
  - Docker container สำหรับรัน tests
  - Unit testing with HTML reports
  - Coverage reports
  - Test results archiving

### การตั้งค่า Jenkins:
1. สร้าง Pipeline job ใหม่
2. เลือก "Pipeline script from SCM"
3. ระบุ Git repository URL
4. Script path: `Jenkinsfile`

## Test Coverage

Test suite ประกอบด้วย 2 ส่วนหลัก:

### 1. Data Transformation Tests (`test_data_cleaning.py`)
- ✅ การแทนที่ null ใน emp_length ด้วย 'N/A'
- ✅ การกรอง application_type '<NA>'
- ✅ การแปลง issue_d เป็น datetime
- ✅ การแปลง int_rate จาก % string เป็น float
- ✅ การรักษา data integrity

### 2. Data Quality Tests (`test_data_quality.py`)
- ✅ Dimension tables ไม่มี duplicate values
- ✅ Foreign keys ใน fact table มีอยู่จริงใน dimensions
- ✅ Loan amounts เป็นค่าบวก
- ✅ Funded amount ไม่เกิน loan amount
- ✅ Interest rate อยู่ในช่วง 0-1

**รวม: 10 test cases** ครอบคลุมทั้ง data transformation และ star schema integrity

## Development Workflow

1. สร้าง feature branch:
```bash
git checkout -b feature/your-feature
```

2. พัฒนาและทดสอบ:
```bash
# แก้ไขโค้ด
# รัน tests
pytest tests/ -v
```

3. Commit และ push:
```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

4. สร้าง Pull Request
5. รอ CI pass
6. Merge เมื่อได้รับการ review

## ข้อกำหนดระบบ

- Python 3.8+
- SQL Server (สำหรับรัน ETL จริง - ไม่จำเป็นสำหรับรัน tests)
- Docker (สำหรับ Jenkins CI)
- Git

## การแก้ปัญหา

### pytest import error:
```bash
# ตรวจสอบ PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Permission denied ใน Jenkins:
```bash
# ให้สิทธิ์ execute
chmod +x Jenkinsfile
```

## License

MIT License
