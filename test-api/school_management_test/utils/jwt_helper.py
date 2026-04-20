# # token 解析
import jwt
import json
from config import BASE_URL  # 实际应从配置文件读取 JWT_SECRET
# 注意：需要与后端 JWT 密钥一致
JWT_SECRET = "your-256-bit-secret-key-for-jwt-signature-here"  # 从 application.yml 复制

def decode_token(token):
    """解析 JWT token，返回 payload dict"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception as e:
        raise ValueError(f"Token 解析失败: {e}")