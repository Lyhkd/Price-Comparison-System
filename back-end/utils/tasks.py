import requests
from celery import current_app as celery  # 核心是这句

@celery.task(name='fetch_price')
def fetch_price(url):
    """
    爬取商品价格的示例任务
    """
    try:
        response = requests.get(url, timeout=10)  # 模拟发送 HTTP 请求
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        # 假设返回的数据包含商品名称和价格
        return {
            "product_name": data.get("title", "未知商品"),
            "price": data.get("price", "未知价格")
        }
    except Exception as e:
        return {"error": str(e)}

@celery.task(name='simple/add2')
def add2(x, y):
    return x + y

@celery.task(name="send_mail")
def send_mail(to, subject, content):
    """
    发送邮件的示例任务
    """
    message = Message("标题", sender=app.config["MAIL_USERNAME"], recipients=["****@qq.com"])
    message.body = "内容"
    mail.send(message)

    return "发送成功"
