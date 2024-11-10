import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yuer0822@localhost:3306/pricecomp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Cookie:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'data/cookie.txt'), 'r') as f:
            self.cookie = f.read()