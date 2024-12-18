import requests, json
from bs4 import BeautifulSoup
import openpyxl
from time import sleep, time


# 基类，后续可以在此之上扩展
class AbstractWebPage:
    def __init__(self, cookie, use_cookie=True):
        if use_cookie:
            self.headers = {
                'authority': 'www.gwdang.com',
                'referer': 'https://www.gwdang.com/',
                'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', 
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cookie': cookie}
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'
            }
        self.sess = requests.session()
        self.sess.headers.update(self.headers)


# 目录类，用来表示搜索结果
class Content(AbstractWebPage):
    def __init__(self, cookie, keyword, end_page):
        super(Content, self).__init__(cookie)
        start_url = 'https://www.gwdang.com/search?crc64='
        self.url_list = [start_url + str(j) + '&s_product=' + keyword for j in range(1, end_page + 1)]
        self.end_page = end_page

    def print(self):
        print(self.url_list, sep='\n')

    def get_item_info_xslx(self):
        wb = openpyxl.load_workbook("/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/good_info2.xlsx")
        ws = wb.active  # 默认获取活动工作表，如果有多个工作表，可以通过 wb[sheet_name] 获取指定工作表

        # 确保表头存在，如果没有表头，添加表头
        if ws.max_row == 1:  # 表格只有一行，说明是新表格，添加表头
            ws.append(["sku", "title", "link", "price", "shop", "img_url"])

        # 写分隔线


        for url in self.url_list:
            res = self.sess.get(url)
            res = res.text
            with open("good_info.html", 'w') as f:
                f.write(res)
            soup = BeautifulSoup(res, 'html.parser').select('[class="dp-list"]')
            # 定位搜索结果主体，并获取所有的商品的标签
            good_list = soup[0].select('li')
            print("get good_list", len(good_list))
            # 循环获取所有商品信息
            for temp in good_list:
                # sku
                sku = temp.get('data-dp-id').strip().split('-')[0]
                good_info = [sku]
                commit_start_url = f'https://item.jd.com/{sku}.html'


                # 获取名称信息
                name_div = temp.select_one('[class="item-title"]')
                name = name_div.text.strip()
                good_info.append(name)
                
                # 商品链接
                good_info.append(commit_start_url)

                # 价格信息
                price_div = temp.select_one('[class=bigRedPrice]')
                good_info.append(price_div.text.strip())

                # 店铺信息
                shop_div = temp.select_one('[class=site]')
                good_info.append(shop_div.get_text().strip())
                # good_info.append("https:"+shop_div.select_one('a').get('href'))
                
                
                # 图片信息
                item_url = temp.select_one('[class=item-img]').select_one('img').get('src')
                good_info.append(item_url)

                # 将商品信息写入到Excel
                ws.append(good_info)

        # 保存Excel文件
        wb.save("good_info2.xlsx")

if __name__ == "__main__":
    # cookie，用于验证登录状态，必须要有cookie，否则京东会提示网络繁忙请重试
    # 获取方法：使用浏览器登录过后按F12，点击弹出界面中最上方的network选项，name栏里面随便点开一个，拉到最下面就有cookie，复制到cookie.txt中
    # 注意，不要换行，前后不要有空格，只需要复制cookie的值，不需要复制“cookie：”这几个字符
    # 上面的看不懂的话，看这个：https://blog.csdn.net/qq_46047971/article/details/121694916
    # 然后就可以运行程序了
    cookie_str = ''
    with open('/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/gwdown_cookie.txt') as f:
        cookie_str = f.readline()
    # cookie_str += 'GWD_USER_TIME=' + str(int(time())) + ';'
    # 输入cookie，关键词，输入结束页数
    content_page = Content(cookie_str, '手机', 1)
    content_page.print()

    content_page.get_item_info_xslx()
    # content_page.get_detail()
    # content_page.get_price()


