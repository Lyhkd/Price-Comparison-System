from . import celery_bp
from utils.tasks import add2
# from run import test_bp
@celery_bp.route('/test', methods=['GET'])
def index():
    results = add2.delay(3, 5)
    return str(results.wait())