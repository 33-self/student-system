import pytest
import requests
from config import BASE_URL, TEST_USERNAME, TEST_PASSWORD
from utils.db_helper import delete_test_user, execute_sql

@pytest.fixture(scope="function")
def clean_user():
    """每个测试前后清理测试用户（123456）"""
    delete_test_user(TEST_USERNAME)
    yield
    delete_test_user(TEST_USERNAME)

@pytest.fixture(scope="module")
def registered_user():
    """模块级：注册一个用户供登录测试"""
    delete_test_user(TEST_USERNAME)
    url = f"{BASE_URL}/api/auth/register"
    requests.post(url, json={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    yield TEST_USERNAME
    delete_test_user(TEST_USERNAME)

@pytest.fixture
def api_client():
    class ApiClient:
        def __init__(self, base_url):
            self.base_url = base_url
        def post(self, path, **kwargs):
            return requests.post(f"{self.base_url}{path}", **kwargs)
    return ApiClient(BASE_URL)

@pytest.fixture
def clean_csv_user():
    """清理CSV测试用例中的用户"""
    from utils.data_loader import CSV_DATA
    usernames_to_clean = set()
    for case in CSV_DATA:
        username = case.get('username', '')
        if username:
            usernames_to_clean.add(username)
    
    for username in usernames_to_clean:
        delete_test_user(username)
    yield
    for username in usernames_to_clean:
        delete_test_user(username)

def pytest_configure(config):
    """pytest启动时加载CSV数据到DATA"""
    from utils.data_loader import DATA, load_csv_test_data
    DATA['csv_data'] = load_csv_test_data()
