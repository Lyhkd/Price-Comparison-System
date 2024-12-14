from . import db
from datetime import datetime

class PriceAlert(db.Model):
    __tablename__ = 'price_alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    enable = db.Column(db.Boolean, default=True)
    check_interval = db.Column(db.Integer, default=15) # 单位：分钟
    notification_method = db.Column(db.String(50), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'item_id', name='uix_user_item'),
    )
    
class AlertHistory(db.Model):
    __tablename__ = 'alert_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_id = db.Column(db.Integer, db.ForeignKey("price_alerts.id"), nullable=False)
    # price_before = db.Column(db.Numeric(10, 2), nullable=False)
    price_after = db.Column(db.Numeric(10, 2), nullable=False)
    # notification_status = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key
    # alert = db.relationship('PriceAlert', backref='alert_history', cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_alert', 'alert_id'),
        db.Index('idx_created_at', 'created_at'),
    )