from flask import Flask
from flask_cors import CORS
from config import Config
# from routes import api
# from models import db
# from routes import *
init = False


app = Flask(__name__)
app.config.from_object(Config) # 加载配置
CORS(app)  # 允许跨域请求
# 初始化数据库


if __name__ == '__main__':
    app.run(debug=True)