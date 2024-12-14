from . import celery_bp
from utils.tasks import check_price
# from run import test_bp
@celery_bp.route('/test', methods=['GET'])
def index():
    results = check_price.delay()
    return str(results.wait())