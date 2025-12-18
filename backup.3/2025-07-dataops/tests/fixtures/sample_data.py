"""
Mock data สำหรับทดสอบ
ไฟล์นี้เก็บข้อมูลตัวอย่างสำหรับใช้ในการทดสอบ
"""

import pandas as pd

def get_sample_loan_data():
    """สร้างข้อมูล loan ตัวอย่างสำหรับทดสอบ"""
    data = {
        'application_type': ['Individual', 'Joint App', '<NA>', 'Individual', 'Joint App', 'Individual'],
        'annual_inc': [50000, 75000, 60000, 45000, 80000, 55000],
        'annual_inc_joint': [None, 120000, None, None, 150000, None],
        'dti': [15.5, 22.3, 18.7, 25.0, 20.1, 19.5],
        'dti_joint': [None, 18.5, None, None, 16.2, None],
        'emp_length': ['10+ years', None, '< 1 year', '5 years', None, '3 years'],
        'issue_d': ['Jan-2018', 'Feb-2018', 'Mar-2018', 'Apr-2018', 'May-2018', 'Jun-2018'],
        'int_rate': ['10.25%', '15.50%', '8.75%', '12.00%', '9.99%', '11.50%'],
        'home_ownership': ['RENT', 'MORTGAGE', 'OWN', 'RENT', 'MORTGAGE', 'OWN'],
        'loan_status': ['Current', 'Current', 'Fully Paid', 'Current', 'Charged Off', 'Current'],
        'loan_amnt': [10000, 20000, 15000, 8000, 25000, 12000],
        'funded_amnt': [10000, 20000, 15000, 8000, 25000, 12000],
        'installment': [339.31, 641.59, 489.95, 265.68, 789.45, 398.55]
    }
    return pd.DataFrame(data)

def get_edge_case_data():
    """สร้างข้อมูล edge cases สำหรับทดสอบ"""
    data = {
        'all_na_application': {
            'application_type': ['<NA>', '<NA>', '<NA>'],
            'emp_length': ['10+ years', '5 years', '< 1 year'],
            'issue_d': ['Jan-2018', 'Feb-2018', 'Mar-2018'],
            'int_rate': ['10.25%', '15.50%', '8.75%'],
        },
        'missing_columns': {
            'application_type': ['Individual', 'Joint App'],
            'emp_length': ['10+ years', None],
            # ไม่มี issue_d และ int_rate
        },
        'already_clean': {
            'application_type': ['Individual', 'Joint App'],
            'emp_length': ['10+ years', '5 years'],  # ไม่มี null
            'issue_d': pd.to_datetime(['2018-01-01', '2018-02-01']),  # already datetime
            'int_rate': [0.1025, 0.1550],  # already float
        }
    }
    return {key: pd.DataFrame(val) for key, val in data.items()}
