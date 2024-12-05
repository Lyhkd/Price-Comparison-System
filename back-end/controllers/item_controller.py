from models import db
from models.item import Item
from controllers.platform_controller import get_platform_id, get_platform_name
from utils.crawler import Crawler
from app.config import Cookie
from datetime import datetime, timezone
import jieba
from sqlalchemy import text
import re
from controllers.price_controller import get_price_history, add_item_price_history

cookie = Cookie()
crawler = Crawler(cookie.cookie)

def get_random_items(page_size):
    items = db.session.query(Item).order_by(db.func.random()).limit(page_size).all()
    serialized_items = [Item.serialize(item) for item in items]
    for item in serialized_items:
        item['platform'] = get_platform_name(item['platform'])
    return {
        "total": page_size,
        "pageSize": page_size,
        "pageNo": 1,
        "totalPages": 1,
        "items": serialized_items
    }

def get_item_details(item_id):
    item = db.session.query(Item).filter_by(id=item_id).first()
    if item is None:
        return None
    if item.description is None:
        item.description = crawler.get_detail_string(item.sku)
        db.session.commit()
    results = {
        'title': item.title,
        'link': item.link,
        'image_url': item.image_url,
        'current_price': item.current_price,
        'shop': item.shop,
        'shop_link': item.shop_link,
        'platform': get_platform_name(item.platform_id),
        'description': item.description
    }
    return results

def segment_text(text):
    # 使用jieba进行中文分词
    return ' '.join(jieba.cut(text))  # 分词结果以空格连接

def is_sku_exists(sku):
    return db.session.query(Item).filter_by(sku=sku, platform_id=get_platform_id('JD')).first() is not None

def update_item(sku, price, keyword):
    item = db.session.query(Item).filter_by(sku=sku).first()
    item.current_price = price
    item.search_title = (keyword+' '+item.search_title)[:255]
    item.update_time = datetime.now(timezone.utc)
    db.session.commit()
    print('update item', item.id)
    add_item_price_history(item)
    
    

def add_item(result, keyword=''):
    search_title = (keyword+' '+segment_text(result['title']))[:255]
    platfrom_id = get_platform_id('JD')
    item = Item(
        title=result['title'],
        search_title=search_title,  # 假设 search_title 就是名称
        link=result['link'],
        image_url=result.get('img_url'),
        current_price=result.get('price'),
        platform_id=platfrom_id,
        shop=result.get('shop'),
        shop_link=result.get('shop_link'),
        sku=result.get('sku')
        )
    db.session.add(item)
    db.session.commit()
    add_item_price_history(item)

def get_total_count(keyword):
    query = text("""
        SELECT COUNT(*) 
        FROM items 
        WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
    """)
    result = db.session.execute(query, {'keyword': keyword})
    total_count = result.scalar()  # 获取查询结果的单一数值
    return total_count

def fulltextsearch(keyword, page_number, page_size, max_size=None):
    offset = (page_number - 1) * page_size  # 计算跳过的记录数
    if max_size is None:
        query = text("""
        SELECT * 
        FROM items 
        WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
        LIMIT :page_size OFFSET :offset
    """)
        result = db.session.execute(query, {'keyword': keyword, 'page_size': page_size, 'offset': offset})
    # 使用LEAST函数限制返回的数量，确保不会超过 max_size
    else: 
        query = text("""
            SELECT * 
            FROM items 
            WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
            LIMIT LEAST(:page_size, :max_size) OFFSET :offset
        """)
    # 执行查询并传入参数
        result = db.session.execute(query, {
            'keyword': keyword,
            'page_size': page_size,  # 每页大小
            'max_size': max_size,    # 最大返回数量限制
            'offset': offset         # 当前分页的偏移量
        })
    
    # 获取查询结果
    return result.fetchall()



def search_items_indb_pagination(keyword, page_number, page_size,max_size=None):
    print(f"begin search page {page_number} page size {page_size} for keyword {keyword}")
    total_count = get_total_count(keyword)
    print(f"total count is {total_count}")
    total_pages = (total_count + page_size - 1) // page_size  # 计算总页数，向上取整
    items = fulltextsearch(keyword, page_number, page_size, max_size)
    serialized_items = [Item.serialize(item) for item in items]
    for item in serialized_items:
        item['platform'] = get_platform_name(item['platform'])
    print(f"get {len(serialized_items)} items from database for keyword {keyword}")
    return {
        "total": total_count,
        "pageSize": page_size,
        "pageNo": page_number,
        "totalPages": total_pages,
        "items": serialized_items
    }


def search_items_from_websites(keyword, page_begin=1, page_end=1):
    print('Searching items for keyword:', keyword)
    results = []
    try: # 爬虫抓取数据
        crawler.update_search(keyword, page_begin, page_end)
        # results = crawler.read_good_info_xlsx("/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/good_info2.xlsx")
        results = crawler.get_item_info_dict()
        from run import app
        with app.app_context():
            for result in results:
                match = re.match(r"^\d+(\.\d+)?", result.get('price'))
                if match:
                    result['price'] = float(match.group())
                else:
                    print(f"skip item with {result.get('price')}")
                
                if is_sku_exists(result['sku']):
                    update_item(result['sku'], result['price'], keyword)
                else:
                    add_item(result, keyword)
                    # 添加到数据库
    
    except Exception as e: # 爬虫出错，从数据库中查找
        print('Error:', e, ' Searching items from database')
        
    print(f"get {len(results)} items from websites for keyword {keyword}")
