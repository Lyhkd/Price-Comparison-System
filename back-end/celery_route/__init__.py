from flask import Blueprint

# 创建各个 Blueprint 实例
celery_bp = Blueprint('celery_bp', __name__)
from .test import *