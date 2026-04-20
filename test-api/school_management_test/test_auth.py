import pytest
import requests
import allure
from config import BASE_URL, TEST_USERNAME, TEST_PASSWORD
from utils.db_helper import query_one, execute_sql, delete_test_user
from utils.jwt_helper import decode_token
from utils.data_loader import DATA
import time

# ==================== 注册测试（数据驱动） ====================

@allure.feature("认证模块")
@allure.story("用户注册")
class TestRegisterDataDriven:

    @pytest.mark.p0
    @pytest.mark.parametrize("case", DATA["register"]["positive"])
    def test_register_positive(self, clean_user, case):
        """正向注册用例"""
        allure.dynamic.title(f"正向注册: {case['description']}")
        allure.dynamic.description(f"工号: {case['username']}, 密码复杂度: 高")
        
        with allure.step("发送注册请求"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="请求参数",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证注册结果"):
            assert resp.status_code == case["expected_status"], f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            if case.get("expected_msg"):
                response_text = resp.text.strip()
                assert response_text == case["expected_msg"] or case["expected_msg"] in resp.text, f"期望消息{case['expected_msg']}，实际{resp.text}"
        
        with allure.step("验证数据库记录"):
            user = query_one("SELECT username, role, status FROM `user` WHERE username=%s", (case["username"],))
            assert user is not None, f"数据库中未找到用户{case['username']}"
            assert user["role"] == 0, f"期望role=0，实际{user['role']}"
            assert user["status"] == 1, f"期望status=1，实际{user['status']}"

    @pytest.mark.p1
    @pytest.mark.parametrize("case", DATA["register"]["invalid_username"])
    def test_register_invalid_username(self, clean_user, case):
        """无效工号注册"""
        allure.dynamic.title(f"无效工号测试: {case['description']}")
        
        with allure.step("发送注册请求"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="请求参数",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证错误信息"):
            assert resp.status_code == case["expected_status"], f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            assert case["expected_msg_contains"] in resp.text, f"期望包含'{case['expected_msg_contains']}'，实际响应: {resp.text}"

    @pytest.mark.p1
    @pytest.mark.parametrize("case", DATA["register"]["password_complexity"])
    def test_register_password_complexity(self, clean_user, case):
        """密码复杂度测试"""
        allure.dynamic.title(f"密码复杂度测试: {case['description']}")
        
        with allure.step("发送注册请求"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": TEST_USERNAME, "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="请求参数",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证密码策略"):
            assert resp.status_code == case["expected_status"], f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            if case["expected_status"] == 400:
                assert case["expected_msg_contains"] in resp.text, f"期望包含'{case['expected_msg_contains']}'，实际响应: {resp.text}"

    @pytest.mark.p1
    @pytest.mark.parametrize("case", DATA["register"]["empty_fields"])
    def test_register_empty_fields(self, clean_user, case):
        """空字段测试"""
        allure.dynamic.title(f"空字段测试: {case['description']}")
        
        with allure.step("发送注册请求"):
            url = f"{BASE_URL}/api/auth/register"
            username = case.get("username", TEST_USERNAME)
            password = case.get("password", TEST_PASSWORD)
            payload = {"username": username, "password": password}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="请求参数",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证错误提示"):
            assert resp.status_code == case["expected_status"], f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            assert case["expected_msg_contains"] in resp.text, f"期望包含'{case['expected_msg_contains']}'，实际响应: {resp.text}"

    @pytest.mark.p1
    def test_register_duplicate(self, clean_user):
        """重复工号测试"""
        allure.dynamic.title("重复工号注册测试")
        
        url = f"{BASE_URL}/api/auth/register"
        payload = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
        
        with allure.step("第一次注册"):
            resp1 = requests.post(url, json=payload)
            allure.attach(
                f"状态码: {resp1.status_code}\n响应: {resp1.text}",
                name="第一次注册响应",
                attachment_type=allure.attachment_type.TEXT
            )
            assert resp1.status_code == 200, f"第一次注册应成功，实际状态码{resp1.status_code}"
        
        with allure.step("第二次注册（重复）"):
            resp2 = requests.post(url, json=payload)
            allure.attach(
                f"状态码: {resp2.status_code}\n响应: {resp2.text}",
                name="第二次注册响应",
                attachment_type=allure.attachment_type.TEXT
            )
            assert resp2.status_code == 400, f"重复注册应失败，实际状态码{resp2.status_code}"
            assert "工号已存在" in resp2.text, f"期望'工号已存在'，实际响应: {resp2.text}"

    @pytest.mark.p2
    def test_register_sql_injection(self, clean_user):
        """SQL注入测试"""
        allure.dynamic.title("SQL注入安全测试")
        
        with allure.step("发送SQL注入payload"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": "' OR 1=1 --", "password": TEST_PASSWORD}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="SQL注入payload",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证注入防护"):
            assert resp.status_code in [400, 200], f"状态码应为400或200，实际{resp.status_code}"
            if resp.status_code == 200:
                delete_test_user("' OR 1=1 --")
                user = query_one("SELECT username FROM `user` WHERE username = %s", ("' OR 1=1 --",))
                assert user is None, "SQL注入成功，数据被插入数据库"

    @pytest.mark.p2
    def test_register_response_time(self, clean_user):
        """注册接口性能测试"""
        allure.dynamic.title("注册接口响应时间测试")
        
        with allure.step("测试响应时间"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
            start = time.time()
            requests.post(url, json=payload)
            elapsed = (time.time() - start) * 1000
            
            allure.attach(
                f"响应时间: {elapsed:.2f}ms\n限制: 500ms",
                name="性能数据",
                attachment_type=allure.attachment_type.TEXT
            )
            assert elapsed < 500, f"响应时间{elapsed:.2f}ms超过500ms限制"


# ==================== 登录测试（数据驱动） ====================

@allure.feature("认证模块")
@allure.story("用户登录")
class TestLoginDataDriven:

    @pytest.mark.p0
    @pytest.mark.parametrize("case", DATA["login"]["positive"])
    def test_login_positive(self, registered_user, case):
        """正常登录测试"""
        allure.dynamic.title(f"登录测试: {case['description']}")
        
        with allure.step("发送登录请求"):
            url = f"{BASE_URL}/api/auth/login"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="请求参数",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证登录结果"):
            assert resp.status_code == case["expected_status"], f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            data = resp.json()
            assert "token" in data, "响应中缺少token字段"
            assert data["username"] == case["username"], f"期望username={case['username']}，实际{data.get('username')}"
            
            if case.get("check_token"):
                token = data["token"]
                decoded = decode_token(token)
                allure.attach(
                    str(decoded),
                    name="Token解析结果",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert decoded.get("userId") or decoded.get("sub"), "Token中缺少userId或sub字段"
                assert decoded.get("username") == case["username"], f"Token中username不匹配"
                assert "exp" in decoded, "Token中缺少exp字段"

    @pytest.mark.p1
    @pytest.mark.parametrize("case", DATA["login"]["invalid"])
    def test_login_invalid(self, registered_user, case):
        """异常登录测试"""
        allure.dynamic.title(f"异常登录测试: {case['description']}")
        
        url = f"{BASE_URL}/api/auth/login"
        username = case["username"]
        password = case["password"]
        
        with allure.step("准备测试数据"):
            if case.get("disabled"):
                execute_sql("UPDATE `user` SET status=0 WHERE username=%s", (username,))
                allure.attach(
                    f"账号{username}已禁用",
                    name="前置操作",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        with allure.step("发送登录请求"):
            payload = {"username": username, "password": password}
            resp = requests.post(url, json=payload)
            
            allure.attach(
                str(payload),
                name="请求参数",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"状态码: {resp.status_code}\n响应: {resp.text}",
                name="响应结果",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证错误信息"):
            assert resp.status_code == case["expected_status"], f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            expected_msgs = case["expected_msg_contains"]
            if isinstance(expected_msgs, list):
                assert any(msg in resp.text for msg in expected_msgs), f"期望包含{expected_msgs}之一，实际响应: {resp.text}"
            else:
                assert expected_msgs in resp.text, f"期望包含'{expected_msgs}'，实际响应: {resp.text}"
            
            if case.get("disabled"):
                execute_sql("UPDATE `user` SET status=1 WHERE username=%s", (username,))

    @pytest.mark.p2
    def test_login_concurrent(self, registered_user):
        """并发登录测试"""
        allure.dynamic.title("并发登录性能测试")
        
        with allure.step("执行30次并发登录"):
            import concurrent.futures
            url = f"{BASE_URL}/api/auth/login"
            payload = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
            def login():
                return requests.post(url, json=payload).status_code
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                results = list(executor.map(lambda _: login(), range(30)))
            
            success_count = results.count(200)
            allure.attach(
                f"总请求数: 30\n成功: {success_count}\n失败: {30-success_count}",
                name="并发测试结果",
                attachment_type=allure.attachment_type.TEXT
            )
            assert all(code == 200 for code in results), f"存在失败的请求: {results}"

    @pytest.mark.p2
    def test_login_error_message_consistency(self):
        """错误信息一致性测试"""
        allure.dynamic.title("登录错误信息一致性测试")
        
        with allure.step("创建临时用户"):
            temp_user = "111111"
            delete_test_user(temp_user)
            requests.post(f"{BASE_URL}/api/auth/register", json={"username": temp_user, "password": TEST_PASSWORD})
        
        with allure.step("测试不存在用户"):
            url = f"{BASE_URL}/api/auth/login"
            resp1 = requests.post(url, json={"username": "999999", "password": TEST_PASSWORD})
            allure.attach(
                f"状态码: {resp1.status_code}\n响应: {resp1.text}",
                name="不存在用户响应",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("测试密码错误"):
            resp2 = requests.post(url, json={"username": temp_user, "password": "wrong"})
            allure.attach(
                f"状态码: {resp2.status_code}\n响应: {resp2.text}",
                name="密码错误响应",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("验证错误格式一致性"):
            resp1_json = resp1.json()
            resp2_json = resp2.json()
            assert "error" in resp1_json, "不存在用户响应缺少error字段"
            assert "error" in resp2_json, "密码错误响应缺少error字段"
            delete_test_user(temp_user)


# ==================== 补充测试用例（CSV数据驱动） ====================

@allure.feature("认证模块")
@allure.story("补充测试用例")
class TestSupplementCases:

    @pytest.mark.p1
    @pytest.mark.parametrize("case", [c for c in DATA.get('csv_data', []) if c.get('module') == 'register' and c.get('priority') == 'P1'])
    def test_register_supplement_p1(self, clean_csv_user, case):
        """注册补充测试用例-P1"""
        allure.dynamic.title(f"注册补充: {case['description']}")
        
        with allure.step("发送注册请求"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(str(payload), name="请求参数", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"状态码: {resp.status_code}\n响应: {resp.text}", name="响应结果", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("验证注册结果"):
            assert resp.status_code == int(case["expected_status"]), f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            if case.get("expected_msg_contains"):
                assert case["expected_msg_contains"] in resp.text, f"期望包含'{case['expected_msg_contains']}'，实际: {resp.text}"
        
        if int(case["expected_status"]) == 200:
            with allure.step("验证数据库记录"):
                user = query_one("SELECT username, role, status, password FROM `user` WHERE username=%s", (case["username"],))
                assert user is not None, f"数据库中未找到用户{case['username']}"

    @pytest.mark.p2
    @pytest.mark.parametrize("case", [c for c in DATA.get('csv_data', []) if c.get('module') == 'register' and c.get('priority') == 'P2'])
    def test_register_supplement_p2(self, clean_csv_user, case):
        """注册补充测试用例-P2"""
        allure.dynamic.title(f"注册补充: {case['description']}")
        
        with allure.step("发送注册请求"):
            url = f"{BASE_URL}/api/auth/register"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(str(payload), name="请求参数", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"状态码: {resp.status_code}\n响应: {resp.text}", name="响应结果", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("验证注册结果"):
            assert resp.status_code == int(case["expected_status"]), f"期望状态码{case['expected_status']}，实际{resp.status_code}"

    @pytest.mark.p1
    @pytest.mark.parametrize("case", [c for c in DATA.get('csv_data', []) if c.get('module') == 'login' and c.get('priority') == 'P1'])
    def test_login_supplement_p1(self, registered_user, case):
        """登录补充测试用例-P1"""
        allure.dynamic.title(f"登录补充: {case['description']}")
        
        with allure.step("发送登录请求"):
            url = f"{BASE_URL}/api/auth/login"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(str(payload), name="请求参数", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"状态码: {resp.status_code}\n响应: {resp.text}", name="响应结果", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("验证登录结果"):
            assert resp.status_code == int(case["expected_status"]), f"期望状态码{case['expected_status']}，实际{resp.status_code}"
            if case.get("expected_msg_contains"):
                assert case["expected_msg_contains"] in resp.text, f"期望包含'{case['expected_msg_contains']}'，实际: {resp.text}"
            
            if int(case["expected_status"]) == 200 and "token" in case.get("expected_msg_contains", ""):
                data = resp.json()
                assert "token" in data, "响应中缺少token字段"
                decoded = decode_token(data["token"])
                allure.attach(str(decoded), name="Token解析", attachment_type=allure.attachment_type.TEXT)

    @pytest.mark.p2
    @pytest.mark.parametrize("case", [c for c in DATA.get('csv_data', []) if c.get('module') == 'login' and c.get('priority') == 'P2'])
    def test_login_supplement_p2(self, registered_user, case):
        """登录补充测试用例-P2"""
        allure.dynamic.title(f"登录补充: {case['description']}")
        
        with allure.step("发送登录请求"):
            url = f"{BASE_URL}/api/auth/login"
            payload = {"username": case["username"], "password": case["password"]}
            resp = requests.post(url, json=payload)
            
            allure.attach(str(payload), name="请求参数", attachment_type=allure.attachment_type.TEXT)
            allure.attach(f"状态码: {resp.status_code}\n响应: {resp.text}", name="响应结果", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("验证登录结果"):
            assert resp.status_code == int(case["expected_status"]), f"期望状态码{case['expected_status']}，实际{resp.status_code}"
