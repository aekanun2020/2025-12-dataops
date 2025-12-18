"""
Main ETL Pipeline
ไฟล์หลักสำหรับรัน ETL process ทั้งหมด
"""

import pandas as pd
import sys
from pathlib import Path

# เพิ่ม path เพื่อให้ import modules อื่นได้
sys.path.append(str(Path(__file__).parent))

# Import modules ที่เราสร้าง
from config.database import DB_CONFIG, FILE_CONFIG, CLEANING_CONFIG
from utils.data_types import guess_column_types, correct_column_types
from etl.data_cleaning import remove_high_null_columns, clean_loan_data, select_columns_for_analysis
from etl.dimensions import create_all_dimensions, create_dimension_mappings
from etl.fact_table import create_fact_table, validate_fact_table
from etl.database_loader import load_all_to_database


def main():
    """
    ฟังก์ชันหลักสำหรับรัน ETL pipeline
    """
    print("=== เริ่มต้น ETL Process ===\n")
    
    # 1. อ่านและวิเคราะห์ data types
    print("1. กำลังอ่านไฟล์และวิเคราะห์ data types...")
    success, column_types = guess_column_types(
        FILE_CONFIG['input_file'],
        FILE_CONFIG['delimiter'],
        FILE_CONFIG['has_headers']
    )
    
    if not success:
        print(f"เกิดข้อผิดพลาด: {column_types}")
        return
    
    # แก้ไข data types ให้เหมาะสม
    column_types_corrected = correct_column_types(column_types)
    print(f"   - พบ {len(column_types_corrected)} columns")
    
    # 2. อ่านข้อมูลด้วย data types ที่ถูกต้อง
    print("\n2. กำลังอ่านข้อมูลทั้งหมด...")
    
    # แยก datetime columns ออกมาเพื่อใช้ parse_dates แทน
    datetime_columns = [col for col, dtype in column_types_corrected.items() if dtype == 'datetime64']
    
    # สร้าง dtype dict ใหม่โดยไม่รวม datetime columns
    dtype_for_read = {col: dtype for col, dtype in column_types_corrected.items() if dtype != 'datetime64'}
    
    # อ่านข้อมูลพร้อม parse datetime columns
    raw_df = pd.read_csv(
        FILE_CONFIG['input_file'], 
        dtype=dtype_for_read,
        parse_dates=datetime_columns
    )
    
    # เลือกเฉพาะ columns ที่ต้องการ
    raw_df = select_columns_for_analysis(raw_df)
    print(f"   - จำนวนแถวทั้งหมด: {len(raw_df):,}")
    
    # 3. ทำความสะอาดข้อมูล
    print("\n3. กำลังทำความสะอาดข้อมูล...")
    
    # ลบ columns ที่มี null มากเกินไป
    df_cleaned = remove_high_null_columns(raw_df, CLEANING_CONFIG['max_null_percentage'])
    print(f"   - คงเหลือ {len(df_cleaned.columns)} columns หลังจากลบ high null columns")
    
    # ทำความสะอาดข้อมูล loan
    df_prepared = clean_loan_data(df_cleaned)
    print(f"   - จำนวนแถวหลังทำความสะอาด: {len(df_prepared):,}")
    
    # 4. สร้าง dimension tables
    print("\n4. กำลังสร้าง Dimension Tables...")
    dimensions = create_all_dimensions(df_prepared)
    
    for dim_name, dim_df in dimensions.items():
        print(f"   - {dim_name}: {len(dim_df)} แถว")
    
    # 5. สร้าง fact table
    print("\n5. กำลังสร้าง Fact Table...")
    dimension_mappings = create_dimension_mappings(dimensions)
    fact_table = create_fact_table(df_prepared, dimension_mappings)
    print(f"   - Fact table: {len(fact_table):,} แถว")
    
    # 6. ตรวจสอบความถูกต้อง
    print("\n6. กำลังตรวจสอบความถูกต้อง...")
    validation = validate_fact_table(fact_table, df_prepared)
    print(f"   - จำนวนแถวตรงกัน: {validation['row_count_match']}")
    print(f"   - Null foreign keys: {validation['null_foreign_keys']}")
    
    # 7. โหลดเข้าฐานข้อมูล
    print("\n7. กำลังโหลดข้อมูลเข้าฐานข้อมูล...")
    success = load_all_to_database(dimensions, fact_table, DB_CONFIG)
    
    if success:
        print("\n=== ETL Process เสร็จสมบูรณ์ ===")
    else:
        print("\n=== ETL Process มีข้อผิดพลาดบางส่วน ===")


if __name__ == "__main__":
    # ตั้งค่าการแสดงผลของ pandas
    pd.set_option('display.float_format', '{:.2f}'.format)
    
    # รัน main function
    main()
