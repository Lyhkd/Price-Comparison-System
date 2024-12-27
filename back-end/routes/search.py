from . import api  # 从 __init__.py 导入 'search' Blueprint
from flask import jsonify, request
from controllers import search_items_indb_pagination, search_items_from_websites, get_random_items
from threading import Thread, Lock
import random
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app

limiter = Limiter(
    get_remote_address,
    app=current_app,
    default_limits=["200 per day", "50 per hour"]
)
# 标志变量和锁
@api.route('/search', methods=['GET'])
@limiter.limit("10/minute")  # 每分钟最多10次请求
def search_items():
    try:
        keyword = request.args.get('keyword')
        pageNo = int(request.args.get('pageNo'))
        pageSize = int(request.args.get('pageSize'))
        platform = request.args.get('platform')
        order = request.args.get('order')
    except:
        return jsonify({"message": "参数错误"}), 200
    if not pageNo or not pageSize:
        return jsonify({"code":1, "message": "Keyword is required", "data": []}), 200
    if not keyword:
        items = get_random_items(pageSize)
        return jsonify({"code":0, "message": "Success", "data": items}), 200
    
    items = search_items_indb_pagination(keyword, page_number=pageNo, page_size=pageSize, platform=platform, order=order)
    
    # if len(items['items']) < pageSize:
    #     print(f"数据库数据不足，爬取网页数据")
    #     search_items_from_websites(keyword, page_begin=pageNo, page_end=pageNo+1, platform=platform)
    #     items = search_items_indb_pagination(keyword, page_number=pageNo, page_size=pageSize, platform=platform)
        
    
    
    print("异步启动爬虫抓取更多的数据")
    # 异步启动爬虫抓取更多的数据
    if platform != 'AMAZON':
        pageNo = pageNo + random.randint(1, 5)
        endNo = pageNo + 2
    else :
        pageNo = pageNo
        endNo = pageNo + 5
    thread = Thread(target=search_items_from_websites, args=(keyword, pageNo, endNo, platform))
    thread.start()
    
    if len(items['items']) == 0:
        items = get_random_items(pageSize)
        return jsonify({"code":0, "message": "Success", "data": items}), 200
    
    print("return items", len(items['items']))
    # 返回前端需要的商品信息
    return jsonify({"code":0, "message": "Success", "data": items}), 200



from controllers.item_controller import *
from controllers.price_controller import *
@api.route('/item/<id>', methods=['GET'])
def item_details(id):
    print("receive request for item details")
    try:
        item_id = int(id)
    except ValueError:
        return jsonify({"code": 1, "message": "Invalid params", "data": []}), 200
    
    item = get_item_details(item_id, fetchweb=True)
    if item is None:
        return jsonify({"message": "Item not found"}), 200
    
    description = item.get('description')
    if description is None:
        description = ''
    attrs = parse_description(description)
    
    img_list = attrs.pop('img_list', None)
    img_list = ["https:" + img for img in img_list.split(';')] if img_list else []
    
    data = {
        "id": id,
        "title": item['title'],
        "link": item['link'],
        "imageUrl": item['image_url'],
        "currentPrice": item['current_price'],
        "shop": item['shop'],
        "shopLink": item['shop_link'],
        "platform": item['platform'],
        "attrs": attrs,
        "imgList": img_list
    }
    return jsonify({"code": 0, "message": "Success", "data": data}), 200

@api.route('/item/offline/<id>', methods=['GET'])
def item_update(id):
    print("receive request for item details")
    try:
        item_id = int(id)
    except ValueError:
        return jsonify({"code": 1, "message": "Invalid params", "data": []}), 200
    
    item = get_item_details(item_id, fetchweb=False)
    if item is None:
        return jsonify({"message": "Item not found"}), 200
    
    description = item.get('description')
    if description is None:
        description = ''
    attrs = parse_description(description)
    
    img_list = attrs.pop('img_list', None)
    img_list = ["https:" + img for img in img_list.split(';')] if img_list else []
    
    data = {
        "id": id,
        "title": item['title'],
        "link": item['link'],
        "imageUrl": item['image_url'],
        "currentPrice": item['current_price'],
        "shop": item['shop'],
        "shopLink": item['shop_link'],
        "platform": item['platform'],
        "attrs": attrs,
        "imgList": img_list
    }
    return jsonify({"code": 0, "message": "Success", "data": data}), 200
  
def parse_description(description):
    # 将字符串按空格分割成键值对
    pairs = description.split('\n')
    
    # 将键值对按冒号分割成键和值，并存储在字典中
    attrs = {}
    for pair in pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            attrs[key] = value
    
    return attrs

@api.route('/item/price/<id>', methods=['GET'])
def item_price_history(id):
    try:
        item_id = int(id)
    except:
        return jsonify({"code": 1, "message": "Invalid params", "data":[]}), 200
    price_history = get_price_history(item_id)
    return jsonify({"code": 0, "message": "Success", "data": price_history}), 200