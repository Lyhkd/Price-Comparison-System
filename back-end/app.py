from flask import Flask
from flask_cors import CORS
from models import db
from config import Config
from routes import api

def create_app():
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(Config)
    CORS(app)  # 允许跨域请求
    # 初始化数据库
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(api)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()  # 数据库初始化
    # app.run(debug=True)
