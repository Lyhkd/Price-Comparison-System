import requests, json
from bs4 import BeautifulSoup
from time import sleep
import openpyxl

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
            try:
                good_list = soup[0].select('[class=gl-item]')
            except:
                print('Skip No items found')
                continue
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
            sleep(1)
        # 返回商品字典列表
        return item_list
    
    def get_detail(self, sku=None):
        commit_start_url = f'https://item.jd.com/{sku}.html'
        # 发送请求，得到结果
        res = self.sess.get(commit_start_url)
        price = BeautifulSoup(res.text, 'html.parser').select('[class=price]')
        paras = BeautifulSoup(res.text, 'html.parser').select('[class=p-parameter]')
        pics = BeautifulSoup(res.text, 'html.parser').select('[class=spec-items]')
        pictures = pics[0].select('img')
        parameters = paras[0].select('li')
        # brand = soup[0].select('li')[0].get('title')
        attr = {}
        for parameter in parameters:
            attr[parameter.get_text().split('：')[0]] = parameter.get_text().split('：')[1].strip()
        attr['img_list'] = ""
        for pic in pictures:
            attr['img_list'] += pic.get('src')+";"
        # print(attr)
        return attr
    
    def get_detail_string(self, sku):
        attrs = self.get_detail(sku) 
        if len(attrs.keys()) == 0:
            return None
        # print(attrs)
        results = ''
        for (key, value) in attrs.items():
            results += key+':'+value+'\n'
        return results

    def read_good_info_xlsx(self, file_path):
        """
        从xlsx文件中读取商品信息，并返回字典列表。

        :param file_path: xlsx文件路径
        :return: 包含商品信息的字典列表
        """
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active  # 默认读取活动工作表
        
        # 检查表头
        headers = [cell.value for cell in ws[1]]  # 获取第一行作为表头
        expected_headers = ["sku", "title", "link", "price", "shop", "shop_link", "img_url"]
        if headers != expected_headers:
            raise ValueError(f"表头与预期不符，请检查文件格式！预期表头为: {expected_headers}")

        # 初始化商品信息字典列表
        item_list = []

        # 从第二行开始读取数据
        for row in ws.iter_rows(min_row=2, values_only=True):
            # 将每一行数据转换为字典
            item_info = {
                "sku": row[0],
                "title": row[1].replace('\n', '').replace('\t', '').strip(),
                "link": row[2],
                "price": row[3],
                "shop": row[4],
                "shop_link": row[5],
                "img_url": row[6],
            }
            item_list.append(item_info)
        
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
