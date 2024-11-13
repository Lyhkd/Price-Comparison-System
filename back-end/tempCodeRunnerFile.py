from flask import Flask
from flask_cors import CORS
from config import Config
# from routes import api
from models import db
from routes import *
from sqlalchemy import text

init = False

def db_init(app):
    with app.app_context():
        db.drop_all()
        db.create_all()  # 数据库初始化
        db.session.execute(text('CREATE FULLTEXT INDEX idx_title ON items(search_title);'))
    print('Database initialized')

app = Flask(__name__)
app.config.from_object(Config) # 加载配置
CORS(app)  # 允许跨域请求
# 初始化数据库
db.init_app(app)
# 注册蓝图
app.register_blueprint(api, url_prefix='/api')  # /api/search, /api/login

if __name__ == '__main__':
    if init:
        db_init(app)
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True)