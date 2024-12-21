from flask import Flask
from flask_cors import CORS
from .config import Config
# from routes import api
from models import *
from routes import api
from sqlalchemy import text
from celery import Celery
from app import celeryconfig
from flask_mail import Mail



def register_celery(celery, app):
    class ContextTask(celery.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    
    
def create_app(celery=None,db_init=False,register_celery_blueprint=False):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail = Mail()
    mail.init_app(app)
    CORS(app)
    if celery:
        register_celery(celery=celery, app=app)  # >> 注册celery
    if register_celery_blueprint:
        from celery_route import celery_bp
        app.register_blueprint(celery_bp)
    app.register_blueprint(api)  # /api/search, /api/login # 注册蓝图
    if db_init:
        with app.app_context():
            db.drop_all()
            db.create_all()  # 数据库初始化
            # db.session.execute(text('CREATE FULLTEXT INDEX idx_title ON items(search_title);'))
            db.session.execute(text('ALTER TABLE items ADD FULLTEXT INDEX ngram_index (title) WITH PARSER ngram;'))
            print('Database initialized')
    return app

    
def make_celery(app_name):
    print("celeryconfig.broker_url", celeryconfig.broker_url)
    print("celeryconfig.result_backend", celeryconfig.result_backend)
    celery = Celery(app_name,
                    broker=celeryconfig.broker_url,
                    backend=celeryconfig.result_backend)
    celery.config_from_object(celeryconfig)
    return celery

celery = make_celery(__name__)
app = create_app(celery=celery, db_init=False, register_celery_blueprint=False)