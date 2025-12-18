# Unit Tests

## เงื่อนไขเบื้องต้น: Code ต้อง Modularization

การทำ Unit Testing แบบนี้ได้ **code ต้องถูกออกแบบให้เป็น modular** คือแยก function ออกเป็นชิ้นเล็กๆ ที่ทำหน้าที่เฉพาะ

### หลักการ Modularization

**1. แยก function ตามหน้าที่ (Single Responsibility)**

แทนที่จะเขียน ETL ทั้งหมดในไฟล์เดียว ให้แยกเป็น:
```
etl/
├── data_cleaning.py    # ทำความสะอาดข้อมูลอย่างเดียว
├── dimensions.py       # สร้าง dimension tables อย่างเดียว
├── fact_table.py       # สร้าง fact table อย่างเดียว
└── database_loader.py  # โหลดเข้า database อย่างเดียว
```

**2. Function รับ input และ return output ชัดเจน**

```python
# ดี - test ได้ง่าย
def clean_loan_data(df: pd.DataFrame) -> pd.DataFrame:
    # ทำความสะอาด
    return cleaned_df

# ไม่ดี - test ยาก
def process_everything():
    df = pd.read_csv("data.csv")  # อ่านไฟล์เอง
    # ทำทุกอย่าง
    df.to_sql("table")  # เขียน database เอง
```

**3. แยก configuration ออกจาก logic**

```python
# config/database.py - เก็บค่า config
DB_CONFIG = {'server': '...', 'database': '...'}
FILE_CONFIG = {'input_file': '...'}

# etl/data_cleaning.py - เก็บ logic อย่างเดียว
def clean_loan_data(df):
    # ไม่มี hardcode ค่าใดๆ
```

### ตัวอย่างจากโปรเจคนี้

โปรเจคนี้แยกโครงสร้างเป็น:
```
pre-production/
├── config/
│   └── database.py        # Configuration แยกต่างหาก
├── utils/
│   └── data_types.py      # Utility functions
├── etl/
│   ├── data_cleaning.py   # clean_loan_data() ← test ได้
│   ├── dimensions.py      # create_all_dimensions() ← test ได้
│   ├── fact_table.py      # create_fact_table() ← test ได้
│   └── database_loader.py # load_all_to_database()
└── main.py                # ประกอบร่างทุกอย่าง
```

ทำให้สามารถ test แต่ละ function แยกกันได้:
```python
from etl.data_cleaning import clean_loan_data

def test_emp_length_null_replacement():
    result = clean_loan_data(sample_df)  # เรียก function เดียว
    assert result['emp_length'].isna().sum() == 0  # ตรวจผลลัพธ์
```

---

## เป้าหมายของการทดสอบ

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

## คำสั่งรัน Tests

**รันทั้งหมดพร้อม coverage:**
```bash
./run_all_tests.sh
```

**รันทั้งหมดแบบธรรมดา:**
```bash
pytest tests/ -v
```

**รันพร้อม HTML coverage report:**
```bash
pytest tests/ -v --cov=pre-production/etl --cov-report=html
```
Report จะอยู่ที่ `htmlcov/index.html`

---

## Test Cases

### test_data_cleaning.py

ทดสอบการทำความสะอาดข้อมูล:
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

### test_data_quality.py

ทดสอบความถูกต้องของ Star Schema:
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
