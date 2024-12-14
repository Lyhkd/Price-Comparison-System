from models import db
from models.price_history import PriceHistory
from controllers.platform_controller import get_platform_id
from datetime import datetime

def get_price_history(product_id, platform_id=None, platform_name=None):
    if platform_name is not None:
        platform_id = get_platform_id(platform_name)
    if platform_id is not None:
        price_history = PriceHistory.query.filter_by(item_id=product_id, platform_id=platform_id).all()
    price_history = PriceHistory.query.filter_by(item_id=product_id).all()
    res = []
    for price in price_history:
        date = price.date.strftime("%Y-%m-%d")
        if len(res) > 0 and res[-1]['date'] == date:
            res[-1]['price'] = price.price
        else: 
            res.append({
                'price': price.price,
                'date': date
            })
    return res

def add_price_history(data):
    # data {
    #     item_id: int,
    #     platform_if: int,
    #     price: float
    # }
    item_id = data.get('item_id')
    platform_id = data.get('platform_id')
    price = data.get('price')
    last = PriceHistory.query.filter_by(item_id=item_id, platform_id=platform_id).first()
    last_update_time = last.date
    last_price = last.price
    if last_update_time is not None:
        if (datetime.now() - last_update_time).days < 1 and price == last_price:
            return
        else:
            last.date = datetime.now()
            last.price = price
            db.session.commit()
            return
    price_history = PriceHistory(item_id=item_id, platform_id=platform_id, price=price)
    db.session.add(price_history)
    db.session.commit()
    
    
def add_item_price_history(item):
    # print("add_item_price_history item id", item.id, item.current_price)
    last = PriceHistory.query.filter_by(item_id=item.id, platform_id=item.platform_id).first()
    if last is not None: # 如果已经有记录，且最近一次更新时间在一天内，且价格没有变化，则不添加
        last_update_time = last.date
        last_price = last.price
        if last_update_time is not None:
            if (datetime.now() - last_update_time).days < 1 and item.current_price == last_price:
                print("no need to update price history")
                return
    price_history = PriceHistory(item_id=item.id, platform_id=item.platform_id, price=item.current_price)
    db.session.add(price_history)
    db.session.commit()