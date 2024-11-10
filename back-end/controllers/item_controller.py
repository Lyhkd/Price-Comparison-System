from models import db, Item
from utils import Crawler
from config import Cookie
from datetime import datetime, timezone
import jieba
from sqlalchemy import text
import re

cookie = Cookie()
crawler = Crawler(cookie.cookie)

def segment_text(text):
    # 使用jieba进行中文分词
    return ' '.join(jieba.cut(text))  # 分词结果以空格连接

def is_sku_exists(sku):
    return db.session.query(Item).filter_by(sku=sku, platform='JD').first() is not None

def update_item(sku, price, keyword):
    item = db.session.query(Item).filter_by(sku=sku).first()
    item.current_price = price
    item.search_title = (keyword+' '+item.search_title)[:255]
    item.update_time = datetime.now(timezone.utc)
    db.session.commit()

def add_item(result, keyword=''):
    search_title = (keyword+' '+segment_text(result['title']))[:255]
    
    item = Item(
        title=result['title'],
        search_title=search_title,  # 假设 search_title 就是名称
        link=result['link'],
        image_url=result.get('img_url'),
        current_price=result.get('price'),
        platform='JD',
        shop=result.get('shop'),
        shop_link=result.get('shop_link'),
        sku=result.get('sku')
        )
    db.session.add(item)

# def fulltextsearch(keyword):
#     query = text("SELECT * FROM items WHERE MATCH(search_title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)")
#     result = db.session.execute(query, {'keyword': keyword})
#     return result.fetchall()

def get_total_count(keyword):
    query = text("""
        SELECT COUNT(*) 
        FROM items 
        WHERE MATCH(search_title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
    """)
    result = db.session.execute(query, {'keyword': keyword})
    total_count = result.scalar()  # 获取查询结果的单一数值
    return total_count

def fulltextsearch(keyword, page_number, page_size):
    offset = (page_number - 1) * page_size  # 计算跳过的记录数
    query = text("""
        SELECT * 
        FROM items 
        WHERE MATCH(search_title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
        LIMIT :page_size OFFSET :offset
    """)
    result = db.session.execute(query, {'keyword': keyword, 'page_size': page_size, 'offset': offset})
    return result.fetchall()

def serialize_item(item) -> dict:
    return {
        'id': item.id,
        'defaultImg': item.image_url,  # 映射 image_url 为 defaultImg
        'currentPrice': item.current_price,
        'title': item.title,
        'link': item.link,
        'shopName': item.shop,  # 映射 shop 为 shopName
        'shopLink': item.shop_link,
        'platform': item.platform
    }

def search_items_indb_pagination(keyword, page_number, page_size):
    total_count = get_total_count(keyword)
    total_pages = (total_count + page_size - 1) // page_size  # 计算总页数，向上取整
    items = fulltextsearch(keyword, page_number, page_size)
    serialized_items = [serialize_item(item) for item in items]
    
    return {
        "total": total_count,
        "pageSize": page_size,
        "pageNo": page_number,
        "totalPages": total_pages,
        "items": serialized_items
    }


def search_items_from_websites(keyword, page_begin=1, page_end=1):
    print('Searching items for keyword:', keyword)
    try: # 爬虫抓取数据
        crawler.update_search(keyword, page_begin, page_end)
        results = crawler.get_item_info_dict()
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
        db.session.commit()
    
    except Exception as e: # 爬虫出错，从数据库中查找
        print('Error:', e, ' Searching items from database')
        

