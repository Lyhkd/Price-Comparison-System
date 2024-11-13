# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# 创建 db 实例
db = SQLAlchemy()

# 导入各个模型
from .user import User, Account, PriceAlert
from .item import Item, Price
from .watch import Watch
