"""
ฟังก์ชันสำหรับทำความสะอาดข้อมูล
ไฟล์นี้มีฟังก์ชันต่างๆ สำหรับ clean และ transform ข้อมูล
"""

import pandas as pd


def remove_high_null_columns(df, max_null_percentage=30):
    """
    ลบ columns ที่มี null values เกินเปอร์เซ็นต์ที่กำหนด
    
    Parameters:
    - df: DataFrame
    - max_null_percentage: เปอร์เซ็นต์ null สูงสุดที่ยอมรับได้
    
    Returns:
    - DataFrame ที่ลบ columns แล้ว
    """
    missing_percentage = df.isnull().mean() * 100
    columns_to_keep = missing_percentage[missing_percentage <= max_null_percentage].index.tolist()
    return df[columns_to_keep]


def clean_loan_data(df):
    """
    ทำความสะอาดข้อมูล loan โดยเฉพาะ
    
    Parameters:
    - df: DataFrame ของข้อมูล loan
    
    Returns:
    - DataFrame ที่ clean แล้ว
    """
    # สำเนา DataFrame เพื่อไม่ให้กระทบต้นฉบับ
    df_clean = df.copy()
    
    # ตรวจสอบว่า DataFrame ว่างหรือไม่
    if df_clean.empty:
        return df_clean
    
    # แทนที่ค่า null ใน emp_length ด้วย 'N/A' (ถ้า column นี้มีอยู่)
    if 'emp_length' in df_clean.columns:
        df_clean['emp_length'] = df_clean['emp_length'].fillna('N/A')
    
    # กรองแถวที่ application_type เป็น '<NA>' ออก (ถ้า column นี้มีอยู่)
    if 'application_type' in df_clean.columns:
        df_clean = df_clean[df_clean['application_type'] != '<NA>']
    
    # แปลง issue_d เป็น datetime (ถ้า column นี้มีอยู่)
    if 'issue_d' in df_clean.columns:
        df_clean['issue_d'] = pd.to_datetime(df_clean['issue_d'], format='%b-%Y')
    
    # แปลง int_rate จาก string เป็น float (ถอด % ออก) (ถ้า column นี้มีอยู่)
    if 'int_rate' in df_clean.columns:
        if df_clean['int_rate'].dtype == 'object' or df_clean['int_rate'].dtype == 'string':
            df_clean['int_rate'] = df_clean['int_rate'].str.rstrip('%').astype('float') / 100.0
    
    return df_clean


def select_columns_for_analysis(df):
    """
    เลือกเฉพาะ columns ที่ต้องการสำหรับการวิเคราะห์
    
    Parameters:
    - df: DataFrame
    
    Returns:
    - DataFrame ที่มีเฉพาะ columns ที่ต้องการ
    """
    columns_needed = [
        'application_type', 'annual_inc', 'annual_inc_joint', 
        'dti', 'dti_joint', 'emp_length', 'issue_d', 'int_rate',
        'home_ownership', 'loan_status', 'loan_amnt', 
        'funded_amnt', 'installment'
    ]
    
    # ตรวจสอบว่า columns ที่ต้องการมีอยู่ใน DataFrame
    available_columns = [col for col in columns_needed if col in df.columns]
    
    return df[available_columns]
