# models/item.py
from datetime import datetime
from sqlalchemy import UniqueConstraint, Index
from . import db

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    search_title = db.Column(db.String(255), nullable=False) # mysql不支持中文分词，手动分词后用于搜索的标题
    link = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    current_price = db.Column(db.Float, nullable=False)
    platform = db.Column(db.String(100), nullable=True)
    platform_info = db.relationship('Platform', backref=db.backref('items', lazy=True))
    shop = db.Column(db.String(255), nullable=True)
    shop_link = db.Column(db.String(255), nullable=True)
    sku = db.Column(db.String(255), nullable=True, unique=True)
    __table_args__ = (
        UniqueConstraint('title', 'shop', name='uix_name_shop'),
    )
    def __repr__(self):
        return f'<Item {self.name}>'
    
    def serialize(item) -> dict:
        return {
            'id': item.id,
            'defaultImg': item.image_url,  # 映射 image_url 为 defaultImg
            'currentPrice': item.current_price,
            'title': item.title,
            'link': item.link,
            'shopName': item.shop,  # 映射 shop 为 shopName
            'shopLink': item.shop_link,
            'platform': item.platform
        }

    