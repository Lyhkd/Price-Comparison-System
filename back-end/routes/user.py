from utils.auth import generate_token
from . import api  # 从 __init__.py 导入 'search' Blueprint
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from controllers.user_controller import *
from functools import wraps
from app.config import Config


@api.route('/user/signup', methods=['POST'])
# 用户注册
def Signup():
    data = request.get_json()
    username = data.get('name')
    password = data.get('password')
    email = data.get('email')

    # 检查用户名和邮箱是否存在
    if not username or not password or not email:
        return jsonify({"code":1, "message": "用户名、密码和邮箱不能为空", "data":""}), 400

    if is_user_exist(username):
        return jsonify({"code":1, "message": "用户名已存在", "data":""}), 200
    if is_email_exist(email):
        return jsonify({"code":1, "message": "邮箱已存在", "data":""}), 200
    
    data['password'] = generate_password_hash(password)
    
    try:
        add_user(data)
    except Exception as e:
        return jsonify({"code":1, "message": "注册失败 "+ str(e), "data":""}), 400
    
    return jsonify({"code":0, "message": "注册成功", "data":""}), 201

# 用户登录
@api.route('/user/login', methods=['POST'])
def Login():
    data = request.get_json()
    username = data.get('name')
    password = data.get('password')

    if '@' in username:
        user = email_check(username)
    else:
        user = user_check(username)
 
    if user is not None:
        if check_password_hash(user.password, password):
            token = generate_token(user)
            return jsonify({"code":0, "message": "登录成功", "data": {"token": token}}), 200
        else:
            return jsonify({"code":1, "message": "登录失败，密码错误", "data":""}), 200
        
    return jsonify({"code":1, "message": "登录失败，用户不存在", "data":""}), 200


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            print(token)
            return jsonify({'message': 'Invalid token!'}), 401
        return f(data['username'], *args, **kwargs)
    return decorated_function


@api.route('/user/auth/loginInfo', methods=['PUT'])
@token_required
def updateLoginInfo(username):
    data = request.get_json()
    print(data)
    new_username = data['username'] if 'username' in data else None
    new_email = data['email'] if 'email' in data else None
    new_phone = data['phone'] if 'phone' in data else None
    info = user_check(username)
    if info:
        if new_username:
            info.username = new_username
        if new_email:
            info.email = new_email
        if new_phone:
            info.phone = new_phone
        
        try:
            db.session.commit()
            return jsonify({'code': 0, 'message': 'User info updated successfully', 'data': {
                'username': info.username,
                'email': info.email,
                'phone': info.phone
            }}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'code': 1, 'message': f'Failed to update user info: {str(e)}', 'data': {}}), 500

    return jsonify({'code': 1, 'message': 'User not found', 'data': {}}), 404

@api.route('/user/auth/loginInfo', methods=['GET'])
@token_required
def getLoginInfo(username):
    info = get_login_info(username)
    if info:
        return jsonify({'code': 0, 'message': 'Success', 'data': info}), 200
    return jsonify({'code': 1, 'message': 'User not found', 'data': {}}), 404

# 用户注销
@api.route('/user/logout', methods=['GET'])
def logout():
    return jsonify({'code': 0, 'message': 'Logout success', 'data': {}}), 200

