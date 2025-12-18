"""
ฟังก์ชันสำหรับตรวจสอบประเภทข้อมูล
ไฟล์นี้มีฟังก์ชันสำหรับวิเคราะห์ data types ของแต่ละ column ใน CSV
"""

import re
import pandas as pd


def guess_column_types(file_path, delimiter=',', has_headers=True):
    """
    อ่านไฟล์ CSV และคาดเดา data type ของแต่ละ column
    
    Parameters:
    - file_path: ที่อยู่ของไฟล์ CSV
    - delimiter: ตัวคั่นในไฟล์ (default: ,)
    - has_headers: มี headers หรือไม่ (default: True)
    
    Returns:
    - tuple: (success, column_types หรือ error message)
    """
    try:
        # อ่านไฟล์ CSV
        df = pd.read_csv(file_path, sep=delimiter, low_memory=False, 
                        header=0 if has_headers else None)

        column_types = {}

        # วิเคราะห์ data type ของแต่ละ column
        for column in df.columns:
            # ตรวจสอบว่าเป็น datetime format หรือไม่
            is_datetime = all(re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(value)) 
                            for value in df[column].dropna())

            # ตรวจสอบว่าเป็น date format หรือไม่
            is_date = all(re.match(r'\d{4}-\d{2}-\d{2}', str(value)) 
                        for value in df[column].dropna())

            # กำหนด data type
            if is_datetime:
                inferred_type = 'datetime64'
            elif is_date:
                inferred_type = 'date'
            else:
                inferred_type = pd.api.types.infer_dtype(df[column], skipna=True)

            column_types[column] = inferred_type

        return (True, column_types)
    
    except Exception as e:
        return (False, str(e))


def correct_column_types(column_types):
    """
    แปลง data types ให้เหมาะสมกับ Python และ SQL Server
    
    Parameters:
    - column_types: dictionary ของ column names และ types
    
    Returns:
    - dictionary ที่แก้ไขแล้ว
    """
    corrected = {}
    for col, dtype in column_types.items():
        if dtype == 'date':
            corrected[col] = 'datetime64'
        elif dtype == 'floating':
            corrected[col] = 'float64'
        else:
            corrected[col] = dtype
    
    return corrected
