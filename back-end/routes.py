from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product, Price, PriceAlert, Account

api = Blueprint('api', __name__)

# 用户注册
@api.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if len(username) < 3 or len(username) > 20:
        return jsonify({"message": "用户名长度必须在3到20个字符之间"}), 400
    if len(password) < 6:
        return jsonify({"message": "密码长度必须至少6个字符"}), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "用户名或邮箱已存在"}), 400

    new_user = User(username=username, password_hash=generate_password_hash(password), email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"user_id": new_user.id, "message": "注册成功"}), 201

# 用户登录
@api.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "用户名或密码错误"}), 401

    # 生成 JWT 令牌（可选，需安装 PyJWT）
    # token = jwt.encode({"user_id": user.id}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"user_id": user.id, "message": "登录成功"}), 200

# 商品价格查询
@api.route('/api/search', methods=['GET'])
def search_items():
    query = request.args.get('query', '')
    platforms = request.args.getlist('platforms')  # 支持多个平台查询

    # 这里进行商品查询逻辑，假设从数据库中查询符合条件的商品
    products = Product.query.filter(Product.name.contains(query)).all()
    data = [{"id": product.id, "name": product.name, "category": product.category} for product in products]

    return jsonify({"paging": {"limit": len(data), "offset": 0, "total": len(data)}, "data": data}), 200

# 商品详细信息查询
@api.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    product = Product.query.get(item_id)
    if product is None:
        return jsonify({"message": "商品未找到"}), 404
    return jsonify({"id": product.id, "name": product.name, "category": product.category, "specification": product.specification, "barcode": product.barcode, "image": product.image}), 200

# 添加商品到数据库
@api.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    specification = data.get('specification')
    barcode = data.get('barcode')
    image = data.get('image')

    new_product = Product(name=name, category=category, specification=specification, barcode=barcode, image=image)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"product_id": new_product.id, "message": "商品添加成功"}), 201

# 设置降价提醒
@api.route('/api/price-alert/', methods=['POST'])
def set_price_alert():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = data.get('user_id')
    threshold_price = data.get('threshold_price')
    notification_method = data.get('notification_method')

    new_alert = PriceAlert(product_id=product_id, user_id=user_id, threshold_price=threshold_price, notification_method=notification_method)
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({"message": "降价提醒设置成功"}), 200
