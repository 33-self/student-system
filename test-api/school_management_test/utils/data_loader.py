import yaml
import os
import csv

def load_test_data(file_path=None):
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.yaml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_csv_test_data(file_path=None):
    """加载CSV测试数据"""
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data_supplement.csv')
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

DATA = load_test_data()
CSV_DATA = load_csv_test_data()
