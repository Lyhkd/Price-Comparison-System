from . import api  # 从 __init__.py 导入 'search' Blueprint
from flask import jsonify, request
from controllers import search_items_indb_pagination, search_items_from_websites, get_random_items
from threading import Thread, Lock
import random

# 标志变量和锁
is_searching = False
lock = Lock()
@api.route('/search', methods=['GET'])
def search_items():
    try:
        keyword = request.args.get('keyword')
        pageNo = int(request.args.get('pageNo'))
        pageSize = int(request.args.get('pageSize'))
        platform = request.args.get('platform')
        order = request.args.get('order')
    except:
        return jsonify({"message": "Invalid params"}), 400
    if not pageNo or not pageSize:
        return jsonify({"code":1, "message": "Keyword is required", "data": []}), 400
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
    thread = Thread(target=search_items_from_websites, args=(keyword, pageNo, pageNo+10, platform))
    thread.start()
    
    if len(items['items']) == 0:
        return jsonify({"code":1, "message": "No products found", "data": []}), 404
    
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
    except:
        return jsonify({"code": 1, "message": "Invalid params", data:[]}), 400
    
    item = get_item_details(item_id)
    if item is None:
        return jsonify({"message": "Item not found"}), 404
    attrs = parse_description(item['description'])
    if 'img_list' not in attrs:
        attrs['img_list'] = None
    img_list = attrs['img_list'].split(';') if attrs['img_list'] is not None else []
    img_list = ["https:" + img for img in img_list]
    attrs.pop('img_list')
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
        return jsonify({"code": 1, "message": "Invalid params", "data":[]}), 400
    price_history = get_price_history(item_id)
    return jsonify({"code": 0, "message": "Success", "data": price_history}), 200