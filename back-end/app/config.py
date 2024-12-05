import os
import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yuer0822@localhost:3306/pricecomp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(32)  # 生成一个32字节长度的安全密钥
    CELERY_BROKER_URL='redis://127.0.0.1:6379/1'
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/2'


class Cookie:
    def __init__(self):
        project_root = os.environ.get('PROJECT_ROOT')
        if not project_root:
            raise RuntimeError("PROJECT_ROOT environment variable is not set")
        
        # 构建文件路径
        cookie_file_path = os.path.join(project_root, 'data', 'cookie.txt')
        
        with open(cookie_file_path, 'r') as f:
            self.cookie = f.read()

