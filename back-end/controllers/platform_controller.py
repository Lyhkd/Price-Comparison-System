from models.platform import Platform
from models import db

def is_platform_exist(platform_name):
    platform = Platform.query.filter_by(name=platform_name).first()
    return platform is not None

def get_platform_id(platform_name):
    platform = Platform.query.filter_by(name=platform_name).first()
    return platform.id

def create_platform(platform_name, logo_url=None):
    logo_dict = {
        'JD': "www.jd.com/favicon.ico",
        'TB': "www.taobao.com/favicon.ico"
    }
    platform = Platform(name=platform_name, logo_url=logo_dict[platform_name] if logo_url is None else logo_url)
    db.session.add(platform)
    db.session.commit()