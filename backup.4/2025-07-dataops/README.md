# Loan ETL Pipeline with CI/CD

โปรเจคนี้เป็น ETL (Extract, Transform, Load) pipeline สำหรับข้อมูล loan พร้อมระบบ CI/CD

## โครงสร้างโปรเจค

```
2025-07-dataops/
├── pre-production/        # Source code หลัก
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
- [Unit Tests](./tests/README.md) - เป้าหมายการทดสอบ, คำสั่งรัน, รายละเอียด test cases

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

## ข้อกำหนดระบบ

- Python 3.8+
- SQL Server (สำหรับรัน ETL จริง - ไม่จำเป็นสำหรับรัน tests)
- Docker (สำหรับ Jenkins CI)
- Git
