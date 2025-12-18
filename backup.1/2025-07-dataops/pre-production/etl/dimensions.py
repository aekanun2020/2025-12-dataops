"""
ฟังก์ชันสำหรับสร้าง dimension tables
ไฟล์นี้มีฟังก์ชันสำหรับสร้าง dimension tables ต่างๆ จากข้อมูล
"""

import pandas as pd


def create_dimension_table(df, column_name, dim_name):
    """
    สร้าง dimension table จาก column ที่ระบุ
    
    Parameters:
    - df: DataFrame ต้นฉบับ
    - column_name: ชื่อ column ที่จะใช้สร้าง dimension
    - dim_name: ชื่อของ dimension (ใช้สร้างชื่อ ID column)
    
    Returns:
    - DataFrame ของ dimension table
    """
    # สร้าง dimension table จาก unique values
    dim_df = df[[column_name]].drop_duplicates().reset_index(drop=True)
    
    # เพิ่ม ID column
    dim_df[f'{dim_name}_id'] = dim_df.index
    
    return dim_df


def create_date_dimension(df, date_column):
    """
    สร้าง date dimension table พร้อม month และ year
    
    Parameters:
    - df: DataFrame ต้นฉบับ
    - date_column: ชื่อ column ที่เป็น date
    
    Returns:
    - DataFrame ของ date dimension
    """
    # สร้าง dimension table จาก unique dates
    date_dim = df[[date_column]].drop_duplicates().reset_index(drop=True)
    
    # เพิ่ม month และ year
    date_dim['month'] = date_dim[date_column].dt.month
    date_dim['year'] = date_dim[date_column].dt.year
    
    # เพิ่ม ID column
    date_dim[f'{date_column}_id'] = date_dim.index
    
    return date_dim


def create_all_dimensions(df):
    """
    สร้าง dimension tables ทั้งหมดที่ต้องการ
    
    Parameters:
    - df: DataFrame ที่ clean แล้ว
    
    Returns:
    - dictionary ของ dimension tables
    """
    dimensions = {}
    
    # สร้าง dimension tables ทั่วไป
    dimensions['home_ownership'] = create_dimension_table(df, 'home_ownership', 'home_ownership')
    dimensions['loan_status'] = create_dimension_table(df, 'loan_status', 'loan_status')
    dimensions['application_type'] = create_dimension_table(df, 'application_type', 'application_type')
    dimensions['emp_length'] = create_dimension_table(df, 'emp_length', 'emp_length')
    
    # สร้าง date dimension
    dimensions['issue_d'] = create_date_dimension(df, 'issue_d')
    
    return dimensions


def create_dimension_mappings(dimensions):
    """
    สร้าง mapping dictionaries สำหรับใช้ใน fact table
    
    Parameters:
    - dimensions: dictionary ของ dimension tables
    
    Returns:
    - dictionary ของ mappings
    """
    mappings = {}
    
    for dim_name, dim_df in dimensions.items():
        if dim_name == 'issue_d':
            # สำหรับ date dimension ใช้ column แรกเป็น key
            key_column = dim_df.columns[0]
        else:
            # สำหรับ dimension อื่นๆ ใช้ชื่อเดียวกับ dimension
            key_column = dim_name
            
        id_column = f'{dim_name}_id'
        mappings[dim_name] = dim_df.set_index(key_column)[id_column].to_dict()
    
    return mappings
