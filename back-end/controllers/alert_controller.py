from models import db
from models.price_alert import PriceAlert, AlertHistory
from datetime import datetime, timezone
from sqlalchemy import text

def add_price_alert(data):
    # data {
    #     user_id: int,
    #     item_id: int,
    #     target_price: float,
    #     notification_method: str
    # }
    user_id = data.get('userId')
    item_id = data.get('itemId')
    target_price = data.get('targetPrice')
    notification_method = data.get('notificationMethod')
    if PriceAlert.query.filter_by(user_id=user_id, item_id=item_id).first():
        return False
    alert = PriceAlert(user_id=user_id, item_id=item_id, target_price=target_price, notification_method=notification_method)
    db.session.add(alert)
    db.session.commit()
    return True
    
def query_user_alerts(user_id):
    alerts = PriceAlert.query.filter_by(user_id=user_id).all()
    return alerts


def query_alert(user_id=None, item_id=None, alert_id=None):
    if alert_id:
        alert = PriceAlert.query.get(alert_id)
        return alert
    if user_id and item_id:
        alert = PriceAlert.query.filter_by(user_id=user_id, item_id=item_id).first()
        return alert
    if user_id:
        alerts = PriceAlert.query.filter_by(user_id=user_id).all()
        return alerts
    if item_id:
        alerts = PriceAlert.query.filter_by(item_id=item_id).all()
        return alerts
    return None

def add_alert_history(data):
    # data {
    #     alert_id: int,
    #     price_before: float,
    #     price_after: float,
    #     notification_status: dict
    # }
    alert_id = data.get('alert_id')
    # price_before = data.get('price_before')
    price_after = data.get('price_after')
    # notification_status = data.get('notification_status')
    history = AlertHistory(alert_id=alert_id, price_after=price_after)
    db.session.add(history)
    db.session.commit()
    
    
def query_history(alert_id):
    histories = AlertHistory.query.filter_by(alert_id=alert_id).all()
    return histories

def get_alert_history(alert_id):
    histories = AlertHistory.query.filter_by(alert_id=alert_id).all()
    data = []
    for history in histories:
        data.append({
            "id": history.id,
            # "priceBefore": history.price_before,
            "priceAfter": history.price_after,
            # "notificationStatus": history.notification_status,
            "createAt": history.created_at.isoformat()
        })
    print(data)
    return data