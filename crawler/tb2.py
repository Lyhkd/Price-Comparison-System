import requests
# from pymongo import MongoClient
from urllib.parse import urlencode
import re
import hashlib
import time
from requests.exceptions import RequestException


# conn = MongoClient('127.0.0.1', 27017) # 连接 mongodb
# db = conn.taobao  # 连接taobao数据库，没有则自动创建
# my_set = db.meishi # 连接meishi表，没有则自动创建


# 获取请求需要的信息
def get_request_headers(page, keyword):
    cookie_str = ''
    with open('tb_cookie.txt') as f:
        cookie_str = f.readline()
    page = str(page)
    referer = 'https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=099d87ed80b8f8' \
              '19245aee821810d220&keyword=%E7%BE%8E%E9%A3%9F&page=0'
    headers = {
        'Connection': 'close',
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'cookie': cookie_str
    }
    data = '{"keyword":"%s","ppath":"","loc":"","minPrice":"","maxPrice":"","ismall":"","ship":"","itemAss' \
           'urance":"","exchange7":"","custAssurance":"","b":"","clk1":"099d87ed80b8f819245aee821810d220","p' \
           'voff":"","pageSize":"100","page":"%s","elemtid":"1","refpid":"mm_26632258_3504122_32538762","pid' \
           '":"430673_1006","featureNames":"spGoldMedal,dsrDescribe,dsrDescribeGap,dsrService,dsrServiceGap' \
           ',dsrDeliver, dsrDeliverGap","ac":"X+rWFGryzTMCAUExRJnWSOSi","wangwangid":"' \
           'semir\\\\u7D2B\\\\u98CE","catId":""}' % (keyword, page)
    t = int(time.time()*1000)
    t = str(t)  # 要转化成字符串
    token = "3d843a5726d1c5fae79b96e5527fc27d"
    appkey = "12574478"
    datas = token+'&'+t+'&'+appkey+'&'+data
    sign = hashlib.md5()  # 创建md5对象
    sign.update(datas.encode())  # 使用md5加密要先编码，不然会报错，我这默认编码是utf-8
    signs = sign.hexdigest()   # 加密
    data1 = {
        "jsv": "2.7.2",
        "appKey": "12574478",
        "t": t,  # 上面的t
        "sign": signs,  # 加密之后的值
        "api": "mtop.relationrecommend.wirelessrecommend.recommend",
        "v": "2.0",
        "timeout": "10000",
        # "AntiCreep": "true",
        "type": "jsonp",
        "dataType": "jsonp",
        # "ecode": "0",
        "callback": "mtopjsonp11",
        "data": {
            "keyword": keyword,  # 关键词别忘了
            "ppath": "",
            "loc": "",
            "minPrice": "",
            "maxPrice": "",
            "ismall": "",
            "ship": "",
            "itemAssurance": "",
            "exchange7": "",
            "custAssurance": "",
            "b": "",
            "clk1": "099d87ed80b8f819245aee821810d220",
            "pvoff": "",
            "pageSize": "100",
            "page": page,      # 页码
            "elemtid": "1",
            "refpid": "mm_26632258_3504122_32538762",
            "pid": "430673_1006",
            "featureNames": "spGoldMedal,dsrDescribe,dsrDescribeGap,dsrService,dsrServiceGap,dsrDeliver,2020dsrDeliverGap",  # 2020这里是一个空格
            "ac": "X+rWFGryzTMCAUExRJnWSOSi",
            "wangwangid": "semir\\u7D2B\\u98CE",
            "catId": "",
        }
    }
    # 返回请求头和要传的参数
    return headers, data1


def get_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        print(response.url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException as E:
        print(E)
        return None


def parse_data(data):
    # 使用正则表达式解析数据，经测试其他类型商品数据结构是一样的，这个也能用
    pattern = re.compile('{"dsrDeliver":"(.*?)".*?dsrDescribe":"(.*?)".*?dsrService":"(.*?)".*?eurl":"(.*?)".*?'
                         + 'imgUrl":"(.*?)".*?loc":"(.*?)".*?promoPrice":"(.*?)".*?redkeys":\[(.*?)\].*?title":"(.*?)"'
                         + '.*?wangwangId":"(.*?)"}', re.S)
    datalist = re.findall(pattern, data)
    return datalist


def main():
    keyword = "美食"  # 设置关键词
    for i in range(1, 101):   # 循环一百页
        time.sleep(5)   # 睡5s，降低频率，防止被搞
        page = i
        headers, data1 = get_request_headers(page, keyword)
        data1 = urlencode(data1)  # 将要传输的数据编码 ，这里有个坑，有一个空格编码不出来，只能想换成2020再替换回来
        data1 = re.sub('\+', '', data1)
        data1 = data1.replace('2020', '%20')
        data1 = data1.replace('%27', '%22')
        base_url = 'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?' + data1  #可以用这个完整的url 和页面上的比较，看一不一样，一样就可以了
        datas = get_data(base_url, headers)
        print("get data")
        print(datas)
        if datas is None or datas == []:
            print(page)
            continue
        vallist = parse_data(datas)
        if vallist == []:
            print(page)
            continue
        print(len(vallist))
        for s in vallist:
            data = {
                'title': s[8],
                'img': s[4],
                'price': s[6],
                'xiangxixinxi': s[3],
                'area': s[5],
                'fenlei': s[7],
                'dianpu': s[9],
                'fahuosudu': s[0],
                'shangpinmiaosu': s[1],
                'fuwutaidu': s[2],
            }
            print(data)
            # my_set.insert(data)  # 插入数据


if __name__ == '__main__':
    main()

