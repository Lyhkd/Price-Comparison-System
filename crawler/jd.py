import requests, json
from bs4 import BeautifulSoup


# 基类，后续可以在此之上扩展
class AbstractWebPage:
    def __init__(self, cookie, use_cookie=True):
        if use_cookie:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36',
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
        item_pages_list = []
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

                    # 评价信息
                    # comment_div = temp.select_one('[class=p-commit]').find('strong').find('a')
                    # comment_url = comment_div.get('href')
                    # good_id = comment_url.replace('//item.jd.com/', '').replace('.html#comment', '')
                    # # 评价信息没有在主页面内，而是需要另外发送GET获取，服务器地址如下
                    # # 这里面的uuid是唯一标识符，如果运行程序发现报错或者没有得到想要的结果
                    # # commit_start_url = f'https://api.m.jd.com/?appid=item-v3&functionId' \
                    # #                    '=pc_club_productCommentSummaries&client=pc&clientVersion=1.0.0&t' \
                    # #                    f'=1711091114924&referenceIds={good_id}&categoryIds=9987%2C653%2C655' \
                    # #                    '&loginType=3&bbtf=&shield=&uuid=181111935.1679801589641754328424.1679801589' \
                    # #                    '.1711082862.1711087044.29'
                    # commit_start_url = f'https://api.m.jd.com/?appid=item-v3&functionId' \
                    #                    '=pc_club_productCommentSummaries&client=pc&clientVersion=1.0.0&t' \
                    #                    f'=1711091114924&referenceIds={good_id}&categoryIds=9987%2C653%2C655'
                    # # 发送请求，得到结果
                    # comment_res = self.sess.get(commit_start_url)
                    # # 编码方式是GBK国标编码
                    # comment_res.encoding = 'gbk'
                    # # print("comment res", comment_res.text)
                    # comment_res_json = comment_res.json()

                    # # 解析得到评论数量
                    # good_info += comment_res_json['CommentsCount'][0]['CommentCountStr'] + '\t'

                    # 店铺信息
                    shop_div = temp.select_one('[class=p-shop]')
                    good_info += shop_div.get_text().strip() + '\t'
                    f.write(good_info + '\n')
                    f.write("*" * 50 + '\n')
            f.close()

        return item_pages_list


if __name__ == "__main__":
    # cookie，用于验证登录状态，必须要有cookie，否则京东会提示网络繁忙请重试
    # 获取方法：使用浏览器登录过后按F12，点击弹出界面中最上方的network选项，name栏里面随便点开一个，拉到最下面就有cookie，复制到cookie.txt中
    # 注意，不要换行，前后不要有空格，只需要复制cookie的值，不需要复制“cookie：”这几个字符
    # 上面的看不懂的话，看这个：https://blog.csdn.net/qq_46047971/article/details/121694916
    # 然后就可以运行程序了
    cookie_str = ''
    with open('cookie.txt') as f:
        cookie_str = f.readline()
    
    # 输入cookie，关键词，输入结束页数
    content_page = Content(cookie_str, '手机', 2)
    content_page.print()

    urls = content_page.get_item_info()
    print(urls)
