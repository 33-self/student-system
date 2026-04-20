# 测试数据生成
import random

def generate_username(length=6):
    """生成随机数字工号"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def generate_password():
    """生成符合规则的密码：大小写+数字+特殊符号，长度10"""
    import random
    import string
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")
    rest = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=6))
    password = lower + upper + digit + special + rest
    # 打乱顺序
    lst = list(password)
    random.shuffle(lst)
    return ''.join(lst)