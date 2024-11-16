from datetime import datetime
from . import db

class Platform(db.Model):
    __tablename__ = 'platforms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    logo_url = db.Column(db.String(255))
    