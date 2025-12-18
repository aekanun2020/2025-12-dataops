"""
Test cases สำหรับ clean_loan_data function
ไฟล์นี้ทดสอบการทำความสะอาดข้อมูล loan
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# เพิ่ม path เพื่อ import module จาก pre-production
sys.path.append(str(Path(__file__).parent.parent / 'pre-production'))

from etl.data_cleaning import clean_loan_data


class TestCleanLoanData:
    """Test cases สำหรับ clean_loan_data function"""
    
    @pytest.fixture
    def sample_df(self):
        """สร้าง sample DataFrame สำหรับทดสอบ"""
        data = {
            'application_type': ['Individual', 'Joint App', '<NA>', 'Individual', 'Joint App'],
            'emp_length': ['10+ years', None, '< 1 year', '5 years', None],
            'issue_d': ['Jan-2018', 'Feb-2018', 'Mar-2018', 'Apr-2018', 'May-2018'],
            'int_rate': ['10.25%', '15.50%', '8.75%', '12.00%', '9.99%'],
            'loan_amnt': [10000, 20000, 15000, 8000, 25000],
            'home_ownership': ['RENT', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE']
        }
        return pd.DataFrame(data)
    
    def test_emp_length_null_replacement(self, sample_df):
        """ทดสอบว่า null values ใน emp_length ถูกแทนที่ด้วย 'N/A'"""
        # Arrange
        expected_na_count = sample_df['emp_length'].isna().sum()
        
        # Act
        result_df = clean_loan_data(sample_df)
        
        # Assert
        assert 'N/A' in result_df['emp_length'].values
        assert result_df['emp_length'].isna().sum() == 0
        assert (result_df['emp_length'] == 'N/A').sum() == expected_na_count
    
    def test_application_type_na_filter(self, sample_df):
        """ทดสอบว่า application_type ที่เป็น '<NA>' ถูกกรองออก"""
        # Arrange
        original_count = len(sample_df)
        na_count = (sample_df['application_type'] == '<NA>').sum()
        
        # Act
        result_df = clean_loan_data(sample_df)
        
        # Assert
        assert len(result_df) == original_count - na_count
        assert '<NA>' not in result_df['application_type'].values
    
    def test_issue_d_datetime_conversion(self, sample_df):
        """ทดสอบว่า issue_d ถูกแปลงเป็น datetime"""
        # Act
        result_df = clean_loan_data(sample_df)
        
        # Assert
        assert pd.api.types.is_datetime64_any_dtype(result_df['issue_d'])
        assert result_df['issue_d'].dt.year.min() == 2018
        assert result_df['issue_d'].dt.month.tolist() == [1, 2, 4, 5]  # ไม่มี Mar เพราะถูกกรองออก
    
    def test_int_rate_percentage_conversion(self, sample_df):
        """ทดสอบว่า int_rate ถูกแปลงจาก string % เป็น float"""
        # Act
        result_df = clean_loan_data(sample_df)
        
        # Assert
        assert result_df['int_rate'].dtype == 'float64'
        assert result_df['int_rate'].iloc[0] == 0.1025  # 10.25% -> 0.1025
        assert result_df['int_rate'].iloc[1] == 0.1550  # 15.50% -> 0.1550
        assert all(0 < rate < 1 for rate in result_df['int_rate'])
    
    def test_data_integrity_after_cleaning(self, sample_df):
        """ทดสอบว่าข้อมูลอื่นๆ ยังคงเหมือนเดิมหลังการ clean"""
        # Act
        result_df = clean_loan_data(sample_df)
        
        # Assert
        # ตรวจสอบว่า loan_amnt ยังคงเหมือนเดิม (ยกเว้นแถวที่ถูกกรองออก)
        filtered_original = sample_df[sample_df['application_type'] != '<NA>']
        assert result_df['loan_amnt'].tolist() == filtered_original['loan_amnt'].tolist()
        assert result_df['home_ownership'].tolist() == filtered_original['home_ownership'].tolist()


# สำหรับรันทดสอบแบบ standalone
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
