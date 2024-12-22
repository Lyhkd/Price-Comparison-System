import requests, json
from bs4 import BeautifulSoup
import openpyxl
from time import sleep, time


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
    def get_detail(self, sku=None):
        sku = 100149996442
        commit_start_url = f'https://item.jd.com/{sku}.html'
        # 发送请求，得到结果
        res = self.sess.get(commit_start_url)
        paras = BeautifulSoup(res.text, 'html.parser').select('[class=p-parameter]')
        pics = BeautifulSoup(res.text, 'html.parser').select('[class=spec-items]')
        pictures = pics[0].select('img')
        parameters = paras[0].select('li')
        # brand = soup[0].select('li')[0].get('title')
        attr = {}
        for parameter in parameters:
            attr[parameter.get_text().split('：')[0]] = parameter.get_text().split('：')[1].strip()
        attr['img_plus'] = ""
        for pic in pictures:
            attr['img_plus'] += "https:"+pic.get('src')+";"
        print(attr)
        return parameters
    def get_item_info_xslx(self):
        wb = openpyxl.load_workbook("/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/good_info2.xlsx")
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
                with open("good_info.html", 'w', encoding='utf-8') as f:
                    f.write(res)
                print("retry")
                sleep(10)
                soup = BeautifulSoup(res, 'html.parser').select('#J_goodsList > ul')
            # 定位搜索结果主体，并获取所有的商品的标签
            good_list = soup[0].select('[class=gl-item]')
            print("get good_list", len(good_list))
            # 循环获取所有商品信息
            for temp in good_list:
                # sku
                sku = temp.get('data-sku').strip()
                good_info = [sku]
                commit_start_url = f'https://item.jd.com/{sku}.html'
                # 发送请求，得到结果
                comment_res = self.sess.get(commit_start_url)
                # 编码方式是GBK国标编码
                # comment_res.encoding = 'gbk'
                print(comment_res.text)
                # comment_res_json = comment_res.json()

                # 解析得到评论数量
                # print(comment_res_json['CommentsCount'][0]['CommentCountStr'])
                exit()


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
    def get_price(self, sku=None):
        sku = 100149996442
        t = int(time() * 1000)
        url = f"https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t={t}&body=%7B%22skuId%22%3A{sku}%2C%22"
        url2 = "https://api.m.jd.com/?appid=item-v3&functionId=pctradesoa_recommend&client=pc&clientVersion=1.0.0&t=1733407154469&body=%7B%22methods%22%3A%22accessories%22%2C%22p%22%3A103003%2C%22sku%22%3A100157830530%2C%22cat%22%3A%229987%2C653%2C655%22%2C%22lid%22%3A15%2C%22ck%22%3A%22pin%2CipLocation%2Catw%2Caview%22%2C%22lim%22%3A5%7D&h5st=20241205215914473%3Bhfhhfh55ez1ri4l8%3Bfb5df%3Btk03w19c6198818n3WPQ1813DV30h194DFp-kR9DBPZ3afZ3P_CQ9ZW1R4eEfWd3fqNDio1h5mz4cN93PaZjOr6mK23v%3B62c53cda2185dce0c0cc778823616bb9f93bdde2b1855d2f9298b36377fa1fea%3B4.9%3B1733407154473%3BpjbMhjpd9nIg7jpjxjZf2iFjLrJp-jpd-aYR5mINGWYeDSlRDSlRJrJdJrESJrpjh7pdLDIj9e1TJrpjh7Jjyf4fybldJeVe1ToeKalS2HodJSFf1fVe6PIS1rof7rIjLDIj7SnQEiVS0ipjLDrgJjIeFele2X4T6bYe1flf6PYfFiVS7r4T4H4fyblf5fYfJrJdJfUT1yVTIipjLDrgJTIgyzpe1uWS-GFSMWoRJrJdJTEjLrJp-jJOVWoWKemRyPFSnOHjLDIj_ulS9mFPJrpjh7Jj-WlO9G3TK2HjLDIjFqEjLrJp-3kjLDrfLDIjzXETJrpjLrJp-jJjLDIj0XETJrpjLrJp-roeLDIj1XETJrpjLrJp-rojxjZe2iFjLrpjLDrg7rJdJbYOJipjLrpjh7pdzrJdJfYOJipjLrpjh7Jf_rJdJjYOJipjLrpjh7JjyzZf9rIjLDIj6XETJrpjLrJp-rojxj5R0ipjLrpjh7ZeLDIj46FjLrpjLDrg7rJdJ7FjLrpjLDrg7rJdJb1OJrpjLrJpwqJdJbFQGakNGipjLDrguqpjhjpd0bldKGYfzbFfHWleMaFRJrJdJjoPJrpjLrJpwqJdJrkPJrpjh7Jj0vWe6vmf6rpVLf2YLfVTeqpQGaEQiq5dDe0Q3yVRImVYJrJdJnVO4ipjLD7N%3B10ecfb030f8ed17c8137e619da20f322af0529043f9b36326818a0c2984c828b&x-api-eid-token=jdd03GJYSIMOVXIATBNQOODKDRW2DUP4M6SDWMNMFN5K6RLNHJJULLACJORLTT3PRAH6X53EYTH5FAA4EJTV3NPRL25FRNEAAAAMTS4PBVHYAAAAAC45TEH2NLOQJTQX&loginType=3&uuid=181111935.17310522299991312897114.1731052229.1733393844.1733405264.19"
        res = self.sess.get(url2)
        res.encoding = 'utf-8'
        print(res.text)
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
    content_page = Content(cookie_str, '手机', 3)
    content_page.print()

    content_page.get_item_info_xslx()
    # content_page.get_detail()
    # content_page.get_price()


