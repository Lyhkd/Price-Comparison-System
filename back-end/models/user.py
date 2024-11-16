# models/user.py
from datetime import datetime
from . import db
import string
import secrets

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(8), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)
    avatar = db.Column(db.String(128), nullable=False, default='https://cdn.pixabay.com/photo/2018/11/13/22/01/avatar-3814081_1280.png')
    phone = db.Column(db.String(20), unique=True, nullable=True)
    alert_lists = db.relationship('PriceAlert', backref=db.backref('users', lazy=True))
    search_history = db.relationship('SearchHistory', backref=db.backref('users', lazy=True))
    @staticmethod
    def generate_random_uid(length=8):
        characters = string.ascii_letters + string.digits  # 包含字母和数字
        return ''.join(secrets.choice(characters) for _ in range(length))  # 随机选择字符生成8位UID

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uid:
            self.uid = User.generate_random_uid()  # 自动生成随机的uid


class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    
    user_id = db.Column(db.BigInteger, primary_key=True)
    notification_email = db.Column(db.Boolean, default=True)
    notification_push = db.Column(db.Boolean, default=True)
    notification_wechat = db.Column(db.Boolean, default=False)
    theme = db.Column(db.String(20), default='light')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    user = db.relationship('User', backref='settings', uselist=False)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_user_time', 'user_id', 'created_at'),
    )