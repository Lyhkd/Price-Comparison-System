import requests, json
from bs4 import BeautifulSoup
import openpyxl
from time import sleep


# 基类，后续可以在此之上扩展
class AbstractWebPage:
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


# 目录类，用来表示搜索结果
class Content(AbstractWebPage):
    def __init__(self, cookie, keyword, end_page):
        super(Content, self).__init__(cookie)
        start_url = 'https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8&wq=' + keyword
        self.url_list = [start_url + '&page=' + str(j) for j in range(1, end_page + 1)]
        self.end_page = end_page

    def print(self):
        print(self.url_list, sep='\n')

    def get_item_info(self):
        with open("good_info.txt", 'w', encoding='utf-8') as f:
            f.write("产品名称" + '\t' + '价格' + '\t' + '销量' + '\t' '店铺' + '\n')
            f.write("*" * 50 + '\n')
            for url in self.url_list:
                res = self.sess.get(url)
                res.encoding = 'utf-8'
                res = res.text
                # 定位搜索结果主体，并获取所有的商品的标签
                soup = BeautifulSoup(res, 'html.parser').select('#J_goodsList > ul')
                good_list = soup[0].select('[class=gl-i-wrap]')
                # 循环获取所有商品信息
                for temp in good_list:
                    # 获取名称信息
                    name_div = temp.select_one('[class="p-name p-name-type-2"]')
                    good_info = name_div.text.strip() + '\t'

                    # 价格信息
                    price_div = temp.select_one('[class=p-price]')
                    good_info += price_div.text.strip() + '\t'

                    # 店铺信息
                    shop_div = temp.select_one('[class=p-shop]')
                    good_info += shop_div.get_text().strip() + '\t'
                    f.write(good_info + '\n')
                    f.write("*" * 50 + '\n')
                    
                    # 图片信息
                    img_div = temp.select_one('[class=p-img]')
                    if img_div and img_div.has_attr('src'):
                        img_url = img_div['src']
                        # 处理相对链接的情况
                        if img_url.startswith("//"):
                            img_url = "https:" + img_url
                        good_info.append(img_url)
                    else:
                        good_info.append("无图片链接")
            f.close()
    
    def get_item_info_xslx(self):
        wb = openpyxl.load_workbook("good_info2.xlsx")
        ws = wb.active  # 默认获取活动工作表，如果有多个工作表，可以通过 wb[sheet_name] 获取指定工作表

        # 确保表头存在，如果没有表头，添加表头
        if ws.max_row == 1:  # 表格只有一行，说明是新表格，添加表头
            ws.append(["sku", "title", "link", "price", "shop", "shop_link", "img_url"])

        # 写分隔线


        for url in self.url_list:
            res = self.sess.get(url)
            res.encoding = 'utf-8'
            res = res.text
            soup = BeautifulSoup(res, 'html.parser').select('#J_goodsList > ul')
            while (len(soup) == 0):
                sleep(10)
                soup = BeautifulSoup(res, 'html.parser').select('#J_goodsList > ul')
            # 定位搜索结果主体，并获取所有的商品的标签
            good_list = soup[0].select('[class=gl-item]')
            
            # 循环获取所有商品信息
            for temp in good_list:
                # sku
                sku = temp.get('data-sku').strip()
                good_info = [sku]
                # 获取名称信息
                name_div = temp.select_one('[class="p-name p-name-type-2"]')
                name = name_div.text.strip()
                if name.startswith("自营"):
                    name = name[2:].strip()
                    
                good_info.append(name)
                
                # 商品链接
                item_url = temp.select_one('[class=p-img]').select_one('a').get('href')
                good_info.append("https:"+item_url)

                # 价格信息
                price_div = temp.select_one('[class=p-price]')
                good_info.append(price_div.text.strip()[1:])

                # 店铺信息
                shop_div = temp.select_one('[class=p-shop]')
                good_info.append(shop_div.get_text().strip())
                good_info.append("https:"+shop_div.select_one('a').get('href'))
                
                
                # 图片信息
                img_div = temp.select_one('[class=p-img]').select_one('img')
                img_url = "https:"+img_div.get('data-lazy-img')
                good_info.append(img_url)

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
    with open('/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/cookie.txt') as f:
        cookie_str = f.readline()
    
    # 输入cookie，关键词，输入结束页数
    content_page = Content(cookie_str, '电脑', 3)
    content_page.print()

    content_page.get_item_info_xslx()
