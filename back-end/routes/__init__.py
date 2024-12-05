# routes/__init__.py
from flask import Blueprint

# 创建各个 Blueprint 实例
api = Blueprint('api', __name__)

from .user import *
from .search import *
from .alert import *

# from .item import *
