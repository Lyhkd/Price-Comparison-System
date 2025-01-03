from utils.auth import generate_token
from . import api  # 从 __init__.py 导入 'search' Blueprint
from flask import jsonify, request, current_app
from controllers.alert_controller import *
from controllers.item_controller  import *
from controllers.price_controller import *
from app.config import Config
from flask_mail import Message, Mail

@api.route('/alert', methods=['POST'])
def add_alert():
    data = request.get_json()
    if data.get('targetPrice') is None or data.get('notificationMethod') is None:
        return jsonify({"code":1, "message": "参数缺失", "data":""}), 200
    if add_price_alert(data):
        return jsonify({"code":0, "message": "添加成功", "data":""}), 201
    else:
        return jsonify({"code":1, "message": "添加失败，已存在相同的提醒", "data":""}), 200
    
    
@api.route('/alert/<uid>', methods=['GET'])
def query_alerts(uid):
    alerts = query_alert(user_id=uid)
    data = []
    for alert in alerts:
        details = get_item_details(alert.item_id, fetchweb=False)
        histories = get_alert_history(alert.id)
        price_hist = get_price_history(alert.item_id)
        data.append({
            "id": alert.id,
            "itemId": alert.item_id,
            "title": details.get('title'),
            "imageUrl": details.get('image_url'),
            "currentPrice": details.get('current_price'),
            "enable": alert.enable,
            "targetPrice": alert.target_price,
            "notificationMethod": alert.notification_method,
            "createAt": alert.updated_at.strftime("%Y-%m-%d"),
            "alertHistory" : histories,
            "priceHistory" : price_hist
        })
        
    return jsonify({"code":0, "message": "查询成功", "data":data}), 200


@api.route('/alert/<alertid>', methods=['PUT'])
def update_alert(alertid):
    data = request.get_json()
    alert = query_alert(alert_id=alertid)
    if alert:
        alert.target_price = data.get('targetPrice')
        alert.notification_method = data.get('notificationMethod')
        alert.enable = data.get('enable')
        db.session.commit()
        return jsonify({"code":0, "message": "修改成功", "data":""}), 200
    else:
        return jsonify({"code":1, "message": "修改失败，提醒不存在", "data":""}), 200
    
    
@api.route('/alert/history/<alertid>', methods=['GET'])
def query_alert_history(alertid):
    histories = query_history(alert_id=alertid)
    data = []
    for history in histories:
        data.append({
            "id": history.history_id,
            "priceBefore": history.price_before,
            "priceAfter": history.price_after,
            "notificationStatus": history.notification_status,
            "createAt": history.create_at.strftime("%Y-%m-%d, %H:%M:%S")
        })
    return jsonify({"code":0, "message": "查询成功", "data":data}), 200

@api.route('/alert/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    alert = query_alert(alert_id=alert_id)
    if not alert:
        return jsonify({"code": 1, "message": "未找到相关提醒"}), 200
    db.session.delete(alert)
    db.session.commit()
    return jsonify({"code": 0, "message": "Alert deleted successfully", "data":''}), 200


@api.route('/alert/sendemail', methods=['POST'])
def send_email():
    data = request.get_json()
    message = Message(data['title'], recipients=[data['email']], sender=Config.MAIL_USERNAME, body=data['content'])
    with current_app.app_context():
        mail = Mail()
        mail.send(message)
    return jsonify({"code":0, "message": "发送成功", "data":""}), 200

from twilio.rest import Client
@api.route('/alert/sendsms', methods=['GET'])
def send_sms():
    Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    