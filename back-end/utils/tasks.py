import requests
from celery import current_app as celery  # 核心是这句
from models.price_alert import db, PriceAlert  # 假设你有 AlertList 模型
from flask_mail import Message, Mail
from flask import current_app
from app import Config
from controllers.user_controller import get_user_email, user_check, get_user_phone
from controllers.item_controller import get_item_details
from controllers.alert_controller import add_alert_history, query_alert
from twilio.rest import Client  # 导入 Twilio 客户端
import urllib
import urllib.request

@celery.task(name='simple/add2')
def add2(x, y):
    return x + y

@celery.task(name='alert')
def check_price():
    results = []
    with db.session() as session:  # 使用 Flask 的 SQLAlchemy
        alerts = session.query(PriceAlert).all()  # 查询所有 alertlist 条目
        for alert in alerts:
            if alert.enable is False:
                continue
            current_price = get_item_details(alert.item_id)['current_price']  # 调用爬取价格的逻辑
            print(f"Checking price for product {alert.item_id}, current price: {current_price}, target price: {alert.target_price}")
            if current_price <= alert.target_price:
                print(f"Price for product {alert.item_id} is lower than target price, sending notification...")
                if alert.notification_method == 'email':
                    notify_result = email_notify(alert.user_id, alert.item_id, current_price)
                elif alert.notification_method == 'sms':
                    notify_result = sms_notify(alert.user_id, alert.item_id, current_price)
                results.append({
                    'user_id': alert.user_id,
                    'item_id': alert.item_id,
                    'current_price': current_price,
                    'target_price': alert.target_price,
                    'notify_result': notify_result
                })
    return results
                
def email_notify(user_id, item_id, price):
    title = "[My Price Notification] 您收藏的商品价格下降啦！"
    email = get_user_email(user_id)
    product = get_item_details(item_id)
    alert = query_alert(user_id=user_id, item_id=item_id)
    content =  f"您收藏的商品 {product['title']} 价格已经降到 {price} 元！您预期的价格曾经是 {alert.target_price} 元。\n 点击链接查看详情：{product['link']}"
    print(f"Sending notification to {email} for product {item_id} at price {price}, title: {product['title']}, content: {content}")
    message = Message(title, recipients=[email], sender=Config.MAIL_USERNAME, body=content)
    with current_app.app_context():
        mail = Mail()
        mail.send(message)
    # 这里写通知逻辑，例如发送邮件或短信
    alert.enable = False # 关闭提醒
    add_alert_history({
        'alert_id': alert.id,
        'price_after': price
    })
    print(f"User {user_id} notified for product {item_id} at price {price}.")
    return True

# twilio failed
# def sms_notify(user_id, item_id, price):
#     product = get_item_details(item_id)
#     alert = query_alert(user_id=user_id, item_id=item_id)
#     content = f"您收藏的商品 {product['title']} 价格已经降到 {price} 元！您预期的价格曾经是 {alert.target_price} 元。\n 点击链接查看详情：{product['link']}"
#     print(f"Sending SMS notification to user {user_id} for product {item_id} at price {price}, content: {content}")

#     # 获取用户的手机号码
#     phone_number = "+86"+ get_user_phone(user_id)
#     if not phone_number:
#         print(f"User {user_id} has no phone number, skip sending SMS.")
#         return False
#     # 使用 Twilio 发送短信
#     client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=content,
#         from_=Config.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )
#     print(f"SMS sent to {phone_number}, SID: {message.sid}")
#     alert.enable = False  # 关闭提醒
#     add_alert_history({
#         'alert_id': alert.id,
#         'price_after': price
#     })
#     print(f"User {user_id} notified for product {item_id} at price {price}.")
#     return True

def sms_notify(user_id, item_id, price):
    product = get_item_details(item_id)
    alert = query_alert(user_id=user_id, item_id=item_id)
    if len(product['title']) > 15:
        product['title'] = product['title'][:15] + '...'
    content = f"【云比价】商品{product['title']}价格当前为 {price} 元！您的预期价格为 {alert.target_price} 元。"
    print(f"Sending SMS notification to user {user_id} for product {item_id} at price {price}, content: {content}")

    # 获取用户的手机号码
    phone_number = get_user_phone(user_id)
    if not phone_number:
        print(f"User {user_id} has no phone number, skip sending SMS.")
        return False
    # 使用 Twilio 发送短信
    data = urllib.parse.urlencode({'u': Config.SMS_USER, 'p': Config.SMS_PASSWORD, 'm': phone_number, 'c': content})
    send_url = Config.SMSAPI + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print (Config.SMS_STATUS[the_page])
    alert.enable = False  # 关闭提醒
    # add_alert_history({
    #     'alert_id': alert.id,
    #     'price_after': price
    # })
    print(f"User {user_id} notified for product {item_id} at price {price}.")
    return True

