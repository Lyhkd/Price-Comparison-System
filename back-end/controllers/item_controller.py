from models import db
from models.item import Item
from controllers.platform_controller import get_platform_id, get_platform_name
from utils.crawler import JDCrawler, AmazonCrawler, GWCrawler
from app.config import Cookie
from datetime import datetime, timezone
import jieba
from sqlalchemy import text
import re
from controllers.price_controller import get_price_history, add_item_price_history
import asyncio

cookie = Cookie()
JDcrawler = JDCrawler(cookie.JDcookie)
AZcrawler = AmazonCrawler(cookie.Amazoncookie)
GWcrawler = GWCrawler(cookie.GWcookie)

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
    
def update_item_price(item_id, price):
    item = db.session.query(Item).filter_by(id=item_id).first()
    if item.platform_id == get_platform_id('JD'):
        JDcrawler.update_search(item.search_title)
        results = JDcrawler.get_item_info_dict()
    item.update_time = datetime.now(timezone.utc)
    db.session.commit()
    add_item_price_history(item)


# 获取商品详情
def get_item_details(item_id):
    item = db.session.query(Item).filter_by(id=item_id).first()
    if item is None:
        return None
    if item.description is None or ':' not in item.description:
        if item.platform_id == get_platform_id('JD'):
            # item.description = JDcrawler.get_detail_string(item.sku)
            item.description = asyncio.run(GWcrawler.get_detail_string(item.sku, platform='JD'))
        elif item.platform_id == get_platform_id('AMAZON'):
            item.description = asyncio.run(AZcrawler.get_detail_string(item.sku))
            print("get amazon description", item.description)
            
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
    return db.session.query(Item).filter_by(sku=sku).first() is not None

def update_item(sku, price, keyword=''):
    item = db.session.query(Item).filter_by(sku=sku).first()
    item.current_price = price
    item.search_title = (keyword+' '+item.search_title)[:255] if keyword != '' else item.search_title
    item.update_time = datetime.now(timezone.utc)
    db.session.commit()
    add_item_price_history(item)
    
    
    

def add_item(result, keyword='', platform_name='JD', platform_id=None):
    search_title = (keyword+' '+segment_text(result['title']))[:255]
    if platform_id is None:
        platfrom_id = get_platform_id(platform_name)
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

# 获取搜索结果的总数，分页用
def get_total_count(keyword, platform='all'):
    if platform != 'all':
        query = text(f"""
            SELECT COUNT(*) 
            FROM items 
            WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
            AND platform_id = :platform_id
        """)
        result = db.session.execute(query, {'keyword': keyword, 'platform_id': get_platform_id(platform)})
    else:
        query = text(f"""
            SELECT COUNT(*) 
            FROM items 
            WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
        """)
        result = db.session.execute(query, {'keyword': keyword})
    total_count = result.scalar()  # 获取查询结果的单一数值
    return total_count

def fulltextsearch(keyword, page_number, page_size, max_size=None, platform='all', order='default'):
    offset = (page_number - 1) * page_size  # 计算跳过的记录数
    if order == 'price_asc':
        order_clause = "ORDER BY current_price ASC"
    elif order == 'price_desc':
        order_clause = "ORDER BY current_price DESC"
    else:
        order_clause = ""
        
    if max_size is None:
        if platform != 'all':
            query = text(f"""
            SELECT * 
            FROM items 
            WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
            AND platform_id = :platform_id
            {order_clause}
            LIMIT :page_size OFFSET :offset
        """)
            result = db.session.execute(query, {'keyword': keyword, 'page_size': page_size, 'offset': offset, 'platform_id': get_platform_id(platform)})
        else :
            query = text(f"""
            SELECT * 
            FROM items 
            WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
            {order_clause}
            LIMIT :page_size OFFSET :offset
        """)
            result = db.session.execute(query, {'keyword': keyword, 'page_size': page_size, 'offset': offset})
    # 使用LEAST函数限制返回的数量，确保不会超过 max_size
    else: 
        query = text(f"""
            SELECT * 
            FROM items 
            WHERE MATCH(title) AGAINST(:keyword IN NATURAL LANGUAGE MODE)
            {order_clause}
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



def search_items_indb_pagination(keyword, page_number, page_size,max_size=None, platform='all', order='default'):
    print(f"begin search page {page_number} page size {page_size} for keyword {keyword}")
    total_count = get_total_count(keyword, platform)
    print(f"total count is {total_count}")
    total_pages = (total_count + page_size - 1) // page_size  # 计算总页数，向上取整
    print(platform)
    items = fulltextsearch(keyword, page_number, page_size, max_size, platform, order)
    print("in search items from db len items before filter ", len(items))
    if platform is not None and platform != 'all':
        items = [item for item in items if item.platform_id == get_platform_id(platform)]
        print("after filter ", len(items))
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

is_searching = False
def search_items_from_websites(keyword, page_begin=1, page_end=1, platform='all'):
    global is_searching
    if is_searching:
        return
    is_searching = True
    print('Searching items for keyword:', keyword)
    results = []
    try: # 爬虫抓取数据
        if platform in ['all', 'JD']:
            print('searching JD')
            GWcrawler.update_search(keyword, 'JD', page_begin, page_end)
            results = asyncio.run(GWcrawler.get_item_info_dict())
            JDcrawler.update_search(keyword, page_begin, page_end)
            results += JDcrawler.get_item_info_dict()
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
                        add_item(result, keyword, platform_name='JD')
                        print("add JD item")
                        # 添加到数据库
        if platform in ['all', 'AMAZON']:
            print('searching AMAZON')
            AZcrawler.update_search(keyword, page_begin, page_end)
            results = asyncio.run(AZcrawler.get_item_amazon())
            from run import app
            with app.app_context():
                for result in results:
                    if result.get('price') is None:
                        result['price'] = '0'
                    else: 
                        match = re.match(r"^\d+(\.\d+)?", result.get('price'))
                        if match:
                            result['price'] = float(match.group())
                        else:
                            print(f"skip item with {result.get('price')}")
                    
                    if is_sku_exists(result['sku']):
                        update_item(result['sku'], result['price'], keyword)
                        
                    else:
                        add_item(result, keyword, platform_name='AMAZON')
                        print("add amazon item")
                        # 添加到数据库
    except Exception as e: # 爬虫出错，从数据库中查找
        print('crawler Error:', e, ' Searching items from database')
    print(f"get {len(results)} items from websites for keyword {keyword}")
    is_searching = False



def update_item_price_from_websites(item_id):
    item = db.session.query(Item).filter_by(id=item_id).first()
    results = []
    price = None
    try: # 爬虫抓取数据
        if item.platform_id == get_platform_id('JD'):
            JDcrawler.update_search(item.search_title)
            results = JDcrawler.get_item_info_dict()
        from run import app
        with app.app_context():
            for result in results:
                match = re.match(r"^\d+(\.\d+)?", result.get('price'))
                if match:
                    result['price'] = float(match.group())
                else:
                    print(f"skip item with {result.get('price')}")
                if is_sku_exists(result['sku']):
                    print("find target item and update price ", result['price'])
                    update_item(result['sku'], result['price'])
                else:
                    add_item(result, platform_id=item.platform_id)
                    # 添加到数据库
    except Exception as e: # 爬虫出错，从数据库中查找
        print('Amazon crawler Error:', e, ' Searching items from database')
    if item.platform_id == get_platform_id('JD'):
        price = get_item_details(item_id)['current_price']
    elif item.platform_id == get_platform_id('AMAZON'):
        price = asyncio.run(AZcrawler.get_item_price(item.sku))
        try:
            match = re.match(r"^\d+(\.\d+)?", price)
            if match:
                price = float(match.group())
            else:
                price = None
        except Exception as e:
            print('Amazon crawler Error:', e)
            
        print("get amazon price", price)
        if price is not None:
            from run import app
            with app.app_context():
                update_item(item.sku, price)
        else:
            print("get None price from amazon crawler")
    return price