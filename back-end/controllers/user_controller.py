from models import db
from models.user import User
from datetime import datetime, timezone
import jwt


def is_user_exist(username):
    user = User.query.filter_by(username=username).first()
    return user is not None

def is_email_exist(email):
    user = User.query.filter_by(email=email).first()
    return user is not None

def add_user(data):
    username = data.get('name')
    password = data.get('password')
    email = data.get('email')
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()

def user_check(username):
    user = User.query.filter_by(username=username).first()
    return user

def email_check(email):
    user = User.query.filter_by(email=email).first()
    return user

def get_login_info(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    info = {
        "uid": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "avatar": user.avatar
    }
    return info

def get_user_email(uid):
    user = User.query.get(uid)
    return user.email

def get_user_phone(uid):
    user = User.query.get(uid)
    return user.phone