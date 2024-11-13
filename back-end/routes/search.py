from . import api  # 从 __init__.py 导入 'search' Blueprint
from flask import jsonify, request
from controllers import search_items_indb_pagination, search_items_from_websites
from threading import Thread
import time
# 商品价格查询
@api.route('/search', methods=['GET'])
def search_items():
    try:
        keyword = request.args.get('keyword')
        pageNo = int(request.args.get('pageNo'))
        pageSize = int(request.args.get('pageSize'))
    except:
        return jsonify({"message": "Invalid params"}), 400
    if not keyword or not pageNo or not pageSize:
            return jsonify({"code":1, "message": "Keyword is required", "data": []}), 400
    # search_items_from_websites(keyword, page_begin=pageNo, page_end=pageNo+1)
    items = search_items_indb_pagination(keyword, page_number=pageNo, page_size=pageSize)
    
    if len(items['items']) < pageSize:
        print(f"数据库数据不足，爬取网页数据")
        search_items_from_websites(keyword, page_begin=pageNo, page_end=pageNo+1)
        items = search_items_indb_pagination(keyword, page_number=pageNo, page_size=pageSize)
        
    if len(items['items']) < pageSize:
        return jsonify({"code":1, "message": "No products found", "data": []}), 404
    
    print("searching items from websites")
    # 异步启动爬虫抓取更多的数据
    thread = Thread(target=search_items_from_websites, args=(keyword, pageNo, pageNo+20))
    thread.start()
    
    if not items:
        return jsonify({"code":1, "message": "No products found", "data": []}), 404
    
    print("return items", len(items['items']))
    # 返回前端需要的商品信息
    return jsonify({"code":0, "message": "Success", "data": items}), 200

# @api.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'usertempid, Content-Type'
#     return response