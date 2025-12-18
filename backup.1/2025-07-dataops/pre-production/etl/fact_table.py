"""
ฟังก์ชันสำหรับสร้าง fact table
ไฟล์นี้มีฟังก์ชันสำหรับสร้าง fact table จาก dimensions
"""

import pandas as pd


def create_fact_table(df, dimension_mappings):
    """
    สร้าง fact table โดยใช้ dimension mappings
    
    Parameters:
    - df: DataFrame ที่ clean แล้ว
    - dimension_mappings: dictionary ของ mappings จาก dimension values ไป IDs
    
    Returns:
    - DataFrame ของ fact table
    """
    # สำเนา DataFrame
    fact_df = df.copy()
    
    # Map dimension values ไปเป็น IDs
    for dim_name, mapping in dimension_mappings.items():
        if dim_name in df.columns:
            fact_df[f'{dim_name}_id'] = fact_df[dim_name].map(mapping)
    
    # เลือกเฉพาะ columns ที่ต้องการใน fact table
    fact_columns = [
        # Measures
        'loan_amnt', 'funded_amnt', 'int_rate', 'installment',
        'annual_inc', 'annual_inc_joint', 'dti', 'dti_joint',
        
        # Foreign keys
        'home_ownership_id', 'loan_status_id', 'issue_d_id',
        'application_type_id', 'emp_length_id'
    ]
    
    # กรองเฉพาะ columns ที่มีอยู่จริง
    available_columns = [col for col in fact_columns if col in fact_df.columns]
    
    return fact_df[available_columns]


def validate_fact_table(fact_df, original_df):
    """
    ตรวจสอบความถูกต้องของ fact table
    
    Parameters:
    - fact_df: Fact table DataFrame
    - original_df: DataFrame ต้นฉบับ
    
    Returns:
    - dictionary ของผลการตรวจสอบ
    """
    validation = {}
    
    # ตรวจสอบจำนวนแถว
    validation['row_count_match'] = len(fact_df) == len(original_df)
    validation['fact_rows'] = len(fact_df)
    validation['original_rows'] = len(original_df)
    
    # ตรวจสอบค่า null ใน foreign keys
    fk_columns = [col for col in fact_df.columns if col.endswith('_id')]
    null_counts = {}
    for col in fk_columns:
        null_counts[col] = fact_df[col].isnull().sum()
    validation['null_foreign_keys'] = null_counts
    
    # ตรวจสอบค่า measures ตัวอย่าง
    measure_columns = ['loan_amnt', 'funded_amnt', 'int_rate', 'installment']
    for col in measure_columns:
        if col in fact_df.columns and col in original_df.columns:
            validation[f'{col}_sum_match'] = (
                fact_df[col].sum() == original_df[col].sum()
            )
    
    return validation
