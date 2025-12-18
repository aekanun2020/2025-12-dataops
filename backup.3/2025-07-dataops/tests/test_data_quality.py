"""
Test cases สำหรับ Data Quality ของ Star Schema
ไฟล์นี้ทดสอบความถูกต้องของข้อมูลใน dimension และ fact tables
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# เพิ่ม path เพื่อ import module จาก pre-production
sys.path.append(str(Path(__file__).parent.parent / 'pre-production'))

from etl.dimensions import create_all_dimensions, create_dimension_mappings
from etl.fact_table import create_fact_table
from etl.data_cleaning import clean_loan_data


class TestDataQuality:
    """Test cases สำหรับตรวจสอบ data quality ของ star schema"""
    
    @pytest.fixture
    def sample_cleaned_data(self):
        """สร้าง cleaned data สำหรับทดสอบ"""
        data = {
            'application_type': ['Individual', 'Joint App', 'Individual'],
            'emp_length': ['10+ years', 'N/A', '5 years'],
            'issue_d': pd.to_datetime(['2018-01-01', '2018-02-01', '2018-03-01']),
            'int_rate': [0.1025, 0.1550, 0.0875],
            'home_ownership': ['RENT', 'MORTGAGE', 'OWN'],
            'loan_status': ['Current', 'Fully Paid', 'Current'],
            'loan_amnt': [10000, 20000, 15000],
            'funded_amnt': [10000, 19000, 15000],  # หนึ่งตัวน้อยกว่า loan_amnt
            'installment': [339.31, 641.59, 489.95],
            'annual_inc': [50000, 75000, 60000],
            'annual_inc_joint': [None, 120000, None],
            'dti': [15.5, 22.3, 18.7],
            'dti_joint': [None, 18.5, None]
        }
        return pd.DataFrame(data)
    
    def test_dimension_unique_values(self, sample_cleaned_data):
        """ทดสอบว่า dimension tables ไม่มี duplicate values"""
        dimensions = create_all_dimensions(sample_cleaned_data)
        
        # ตรวจสอบแต่ละ dimension
        for dim_name, dim_df in dimensions.items():
            if dim_name == 'issue_d':
                # issue_d dimension ตรวจสอบ uniqueness ของ date column
                assert dim_df['issue_d'].is_unique, f"{dim_name} มี duplicate dates"
            else:
                # dimension อื่นๆ ตรวจสอบ column แรก
                first_col = dim_df.columns[0]
                assert dim_df[first_col].is_unique, f"{dim_name} มี duplicate values"
    
    def test_fact_foreign_keys_exist(self, sample_cleaned_data):
        """ทดสอบว่าทุก FK ใน fact table มีอยู่ใน dimension tables"""
        dimensions = create_all_dimensions(sample_cleaned_data)
        mappings = create_dimension_mappings(dimensions)
        fact_table = create_fact_table(sample_cleaned_data, mappings)
        
        # ตรวจสอบแต่ละ FK
        for dim_name, dim_df in dimensions.items():
            fk_column = f'{dim_name}_id'
            if fk_column in fact_table.columns:
                # FK values ใน fact ต้องอยู่ใน dimension
                fact_fk_values = fact_table[fk_column].dropna().unique()
                dim_id_values = dim_df[fk_column].unique()
                
                assert all(fk in dim_id_values for fk in fact_fk_values), \
                    f"พบ FK ที่ไม่มีใน {dim_name} dimension"
    
    def test_loan_amount_positive(self, sample_cleaned_data):
        """ทดสอบว่า loan amounts เป็นค่าบวกเสมอ"""
        dimensions = create_all_dimensions(sample_cleaned_data)
        mappings = create_dimension_mappings(dimensions)
        fact_table = create_fact_table(sample_cleaned_data, mappings)
        
        # ตรวจสอบ loan_amnt
        assert all(fact_table['loan_amnt'] > 0), "พบ loan_amnt ที่ไม่ใช่ค่าบวก"
        
        # ตรวจสอบ funded_amnt
        assert all(fact_table['funded_amnt'] > 0), "พบ funded_amnt ที่ไม่ใช่ค่าบวก"
        
        # ตรวจสอบ installment
        assert all(fact_table['installment'] > 0), "พบ installment ที่ไม่ใช่ค่าบวก"
    
    def test_funded_amount_not_exceed_loan(self, sample_cleaned_data):
        """ทดสอบว่า funded_amnt ไม่เกิน loan_amnt"""
        dimensions = create_all_dimensions(sample_cleaned_data)
        mappings = create_dimension_mappings(dimensions)
        fact_table = create_fact_table(sample_cleaned_data, mappings)
        
        assert all(fact_table['funded_amnt'] <= fact_table['loan_amnt']), \
            "พบ funded_amnt ที่มากกว่า loan_amnt"
    
    def test_interest_rate_range(self, sample_cleaned_data):
        """ทดสอบว่า interest rate อยู่ในช่วง 0-1"""
        dimensions = create_all_dimensions(sample_cleaned_data)
        mappings = create_dimension_mappings(dimensions)
        fact_table = create_fact_table(sample_cleaned_data, mappings)
        
        assert all(fact_table['int_rate'] > 0), "พบ int_rate ที่เป็น 0 หรือติดลบ"
        assert all(fact_table['int_rate'] < 1), "พบ int_rate ที่เกิน 100%"


# สำหรับรันทดสอบแบบ standalone
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
