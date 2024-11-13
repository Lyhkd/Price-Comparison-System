import os
import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yuer0822@localhost:3306/pricecomp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(32)  # 生成一个32字节长度的安全密钥


class Cookie:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'data/cookie.txt'), 'r') as f:
            self.cookie = f.read()