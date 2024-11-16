from . import db
from datetime import datetime

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'),nullable=False)
    platform_id = db.Column(db.Integer,db.ForeignKey('platforms.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    # item = db.relationship('Item', backref='price_history', cascade='all, delete-orphan')
    # platform = db.relationship('Platform', backref='price_history', cascade='all, delete-orphan')
    # Indexes
    __table_args__ = (
        db.Index('idx_item_platform', 'item_id', 'platform_id'),
        db.Index('idx_created_at', 'date'),
    )