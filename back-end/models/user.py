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
    avatar = db.Column(db.String(128), nullable=False, default='https://cdn.pixabay.com/photo/2018/11/13/22/01/avatar-3814081_1280.png')
    phone = db.Column(db.String(20), unique=True, nullable=True)
    watch = db.relationship('Watch', backref=db.backref('users', lazy=True))
    @staticmethod
    def generate_random_uid(length=8):
        characters = string.ascii_letters + string.digits  # 包含字母和数字
        return ''.join(secrets.choice(characters) for _ in range(length))  # 随机选择字符生成8位UID

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.uid:
            self.uid = User.generate_random_uid()  # 自动生成随机的uid


class PriceAlert(db.Model):
    __tablename__ = 'price_alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    threshold_price = db.Column(db.Float, nullable=False)
    notification_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    account = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)

