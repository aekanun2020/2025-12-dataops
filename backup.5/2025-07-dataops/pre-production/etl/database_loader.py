"""
ฟังก์ชันสำหรับโหลดข้อมูลเข้าฐานข้อมูล
ไฟล์นี้มีฟังก์ชันสำหรับเชื่อมต่อและโหลดข้อมูลเข้า SQL Server
"""

from sqlalchemy import create_engine
import urllib
import pandas as pd


def create_db_engine(config):
    """
    สร้าง database engine สำหรับเชื่อมต่อ SQL Server
    
    Parameters:
    - config: dictionary ของการตั้งค่า database
    
    Returns:
    - SQLAlchemy engine object
    """
    # สร้าง connection string
    connection_string = (
        f"mssql+pymssql://{config['username']}:{config['password']}"
        f"@{config['server']}/{config['database']}"
    )
    
    # สร้าง engine
    engine = create_engine(connection_string)
    
    return engine


def load_dimension_to_db(dimension_df, table_name, engine):
    """
    โหลด dimension table เข้าฐานข้อมูล
    
    Parameters:
    - dimension_df: DataFrame ของ dimension
    - table_name: ชื่อตารางในฐานข้อมูล
    - engine: SQLAlchemy engine
    
    Returns:
    - bool: สำเร็จหรือไม่
    """
    try:
        # ลบ column 'index' ถ้ามี (จากการ reset_index)
        if 'index' in dimension_df.columns:
            dimension_df = dimension_df.drop(columns=['index'])
        
        # โหลดเข้าฐานข้อมูล
        dimension_df.to_sql(
            table_name, 
            con=engine, 
            if_exists='replace', 
            index=False
        )
        print(f"✓ โหลด {table_name} สำเร็จ ({len(dimension_df)} แถว)")
        return True
        
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการโหลด {table_name}: {str(e)}")
        return False


def load_fact_to_db(fact_df, table_name, engine):
    """
    โหลด fact table เข้าฐานข้อมูล
    
    Parameters:
    - fact_df: DataFrame ของ fact table
    - table_name: ชื่อตารางในฐานข้อมูล
    - engine: SQLAlchemy engine
    
    Returns:
    - bool: สำเร็จหรือไม่
    """
    try:
        # โหลดเข้าฐานข้อมูล
        fact_df.to_sql(
            table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
        print(f"✓ โหลด {table_name} สำเร็จ ({len(fact_df)} แถว)")
        return True
        
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการโหลด {table_name}: {str(e)}")
        return False


def load_all_to_database(dimensions, fact_table, db_config):
    """
    โหลดทั้ง dimensions และ fact table เข้าฐานข้อมูล
    
    Parameters:
    - dimensions: dictionary ของ dimension tables
    - fact_table: DataFrame ของ fact table
    - db_config: dictionary ของการตั้งค่า database
    
    Returns:
    - bool: สำเร็จทั้งหมดหรือไม่
    """
    # สร้าง engine
    engine = create_db_engine(db_config)
    
    success_count = 0
    total_count = 0
    
    # โหลด dimensions
    dimension_table_names = {
        'home_ownership': 'home_ownership_dim',
        'loan_status': 'loan_status_dim',
        'issue_d': 'issue_d_dim',
        'application_type': 'application_type_dim',
        'emp_length': 'emp_length_dim'
    }
    
    print("กำลังโหลด Dimension Tables...")
    for dim_name, dim_df in dimensions.items():
        table_name = dimension_table_names.get(dim_name, f"{dim_name}_dim")
        total_count += 1
        if load_dimension_to_db(dim_df, table_name, engine):
            success_count += 1
    
    # โหลด fact table
    print("\nกำลังโหลด Fact Table...")
    total_count += 1
    if load_fact_to_db(fact_table, 'loans_fact', engine):
        success_count += 1
    
    print(f"\nสรุป: โหลดสำเร็จ {success_count}/{total_count} ตาราง")
    
    return success_count == total_count
