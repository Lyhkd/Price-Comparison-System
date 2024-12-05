import jwt
from datetime import datetime, timezone, timedelta
from app.config import Config

# 1. 准备 Header 和 Payload
header = {
    "alg": "HS256",  # 使用的算法
    "typ": "JWT"     # 类型为 JWT
}

# 用于生成JWT Token
def generate_token(user):
    payload = {
    "username": user.username,  # 用户名
    "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # 设置过期时间（1小时后）
    "iat": datetime.now(timezone.utc)  # 签发时间
}
    token = jwt.encode(
        payload,
        Config.SECRET_KEY,  # 这里的密钥应该放在配置文件中，不要硬编码
        algorithm="HS256",
        headers=header
    )
    return token


