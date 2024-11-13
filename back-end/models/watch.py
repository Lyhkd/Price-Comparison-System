from . import db
from datetime import datetime

class Watch(db.Model):
    __tablename__ = 'watch'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    price_bar = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enable = db.Column(db.Boolean, default=True)
    notification_method = db.Column(db.String(50), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'item_id', name='uix_user_item'),
    )