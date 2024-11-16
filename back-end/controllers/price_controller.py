from models import db
from models.price_history import PriceHistory
from controllers.platform_controller import get_platform_id
from datetime import datetime

def get_price_history(product_id, platform_id=None, platform_name=None):
    if platform_name is not None:
        platform_id = get_platform_id(platform_name)
    if platform_id is not None:
        price_history = PriceHistory.query.filter_by(product_id=product_id, platform_name=platform_name).all()
    price_history = PriceHistory.query.filter_by(product_id=product_id).all()
    return price_history

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
    price_history = PriceHistory(item_id=item.id, platform_id=item.platform_info.id, price=item.current_price)
    db.session.add(price_history)
    db.session.commit()