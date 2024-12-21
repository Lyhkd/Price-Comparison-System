import os
import secrets

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:yuer0822@localhost:3306/pricecomp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(32)  # 生成一个32字节长度的安全密钥
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/1')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/2')
    MAIL_SERVER="smtp.163.com"
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME="MyPrice2025@163.com" # 发送邮箱
    MAIL_PASSWORD="HXZ4P383XwqgpTAk" # 客户端授权码
    TWILIO_ACCOUNT_SID = 'ACa111d45cb5b532f55dcd8159ad273cdd'
    TWILIO_AUTH_TOKEN = '33c2ec522856e127971b8d858f4f3a8a'
    TWILIO_PHONE_NUMBER = '+13613210868'
    SMSAPI = "http://api.smsbao.com/"
    SMS_USER = 'lyhkd'
    SMS_PASSWORD = md5('1234567qaz')
    SMS_STATUS = {
    '0': '短信发送成功',
    '-1': '参数不全',
    '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '余额不足',
    '42': '账户已过期',
    '43': 'IP地址限制',
    '50': '内容含有敏感词'
    }

class Cookie:
    def __init__(self):
        project_root = os.environ.get('PROJECT_ROOT')
        if not project_root:
            raise RuntimeError("PROJECT_ROOT environment variable is not set")
        
        # 构建文件路径
        JD_cookie_file_path = os.path.join(project_root, 'data', 'JDcookie.txt')
        Amazon_cookie_file_path = os.path.join(project_root, 'data', 'Amazoncookie.txt')
        GW_cookie_file_path = os.path.join(project_root, 'data', 'GWcookie.txt')
        
        with open(JD_cookie_file_path, 'r') as f:
            self.JDcookie = f.read()
        with open(Amazon_cookie_file_path, 'r') as f:
            self.Amazoncookie = f.read()
        with open(GW_cookie_file_path, 'r') as f:
            self.GWcookie = f.read()

