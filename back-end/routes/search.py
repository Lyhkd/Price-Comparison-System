from . import api  # 从 __init__.py 导入 'search' Blueprint
from flask import jsonify, request
from controllers import search_items_indb_pagination, search_items_from_websites
# 商品价格查询
@api.route('/search', methods=['GET'])
def search_items():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"code":1, "message": "Keyword is required", "data": []}), 400

    # 调用爬虫抓取数据
    print("searching items from websites")
    search_items_from_websites(keyword, page_begin=request.args.get('pageNo'), page_end=request.args.get('pageNo')+10)
    
    print("searching items from db")
    items = search_items_indb_pagination(keyword, page_number=request.args.get('pageNo'), page_size=request.args.get('pageSize'))
    
    if not items:
        return jsonify({"code":1, "message": "No products found", "data": []}), 404
    
    print("return items", len(items))
    # 返回前端需要的商品信息
    return jsonify({"code":0, "message": "Success", "data": items}), 200
