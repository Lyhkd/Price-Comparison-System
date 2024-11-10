# routes/__init__.py
from flask import Blueprint

# 创建各个 Blueprint 实例
api = Blueprint('api', __name__)

# 导入不同路由文件，这样会自动将路由注册到 Blueprint 中
from . import search