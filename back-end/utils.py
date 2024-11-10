import requests, json
from bs4 import BeautifulSoup


class Crawler(object):
    def __init__(self, cookie, use_cookie=True):
        if use_cookie:
            self.headers = {
                'referer': 'https://search.jd.com/', 
                'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding': 'gzip, deflate, br',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', 
                'cookie': cookie}
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'
            }
        self.sess = requests.session()
        self.sess.headers.update(self.headers)
        
    def update_search(self, keyword, page_begin=1, page_end=1):
        start_url = 'https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8&wq=' + keyword
        self.url_list = [start_url + '&page=' + str(j) for j in range(page_begin, page_end + 1)]
    
    def print(self):
        print(self.url_list, sep='\n')
            
    def get_item_info_dict(self):
        item_list = []  # 用于存储所有商品的字典
        
        for url in self.url_list:
            res = self.sess.get(url)
            res.encoding = 'utf-8'
            res = res.text
            # 定位搜索结果主体，并获取所有的商品的标签
            soup = BeautifulSoup(res, 'html.parser').select('#J_goodsList > ul')
            with open('packet.html', 'w', encoding='utf-8') as f:
                f.write(res)
            good_list = soup[0].select('[class=gl-item]')
            # 循环获取所有商品信息
            for temp in good_list:
                item_info = {}  # 用于存储单个商品的字典
                
                # sku
                sku = temp.get('data-sku').strip()
                item_info['sku'] = sku
                
                # 获取名称信息
                name_div = temp.select_one('[class="p-name p-name-type-2"]').find('em')
                name = name_div.text.replace('\n', '').replace('\t', '').strip()
                
                item_info['title'] = name
                
                # 商品链接
                item_url = temp.select_one('[class=p-img]').select_one('a').get('href')
                item_info['link'] = "https:" + item_url

                # 价格信息
                price_div = temp.select_one('[class=p-price]')
                item_info['price'] = price_div.text.strip()[1:]

                # 店铺信息
                shop_div = temp.select_one('[class=p-shop]')
                item_info['shop'] = shop_div.get_text().strip()
                item_info['shop_link'] = "https:" + shop_div.select_one('a').get('href')
                
                # 图片信息
                img_div = temp.select_one('[class=p-img]').select_one('img')
                img_url = "https:" + img_div.get('data-lazy-img')
                item_info['img_url'] = img_url

                # 将商品信息字典加入列表
                item_list.append(item_info)

        # 返回商品字典列表
        return item_list

    def to_json(self):
        return json.dumps(self.get_item_info_dict(), ensure_ascii=False)

if __name__ == "__main__":
    # cookie，用于验证登录状态，必须要有cookie，否则京东会提示网络繁忙请重试
    # 获取方法：使用浏览器登录过后按F12，点击弹出界面中最上方的network选项，name栏里面随便点开一个，拉到最下面就有cookie，复制到cookie.txt中
    # 注意，不要换行，前后不要有空格，只需要复制cookie的值，不需要复制“cookie：”这几个字符
    # 上面的看不懂的话，看这个：https://blog.csdn.net/qq_46047971/article/details/121694916
    # 然后就可以运行程序了
    cookie_str = ''
    with open('back-end/data/cookie.txt') as f:
        cookie_str = f.readline()
    
    # 输入cookie，关键词，输入结束页数
    content_page = Crawler(cookie_str)
    content_page.update_search('手机', 1)
    
    content_page.print()
    print(content_page.to_json())
    # content_page.get_item_info_xslx()
