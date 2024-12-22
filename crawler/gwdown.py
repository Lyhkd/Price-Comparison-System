import aiohttp
import asyncio
from bs4 import BeautifulSoup
import openpyxl
from urllib.parse import quote

# 基类，后续可以在此之上扩展
class AbstractWebPage:
    def __init__(self, cookie, use_cookie=True):
        if use_cookie:
            self.headers = {
                'authority': 'www.gwdang.com',
                'referer': 'https://www.gwdang.com/',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cookie': cookie
            }
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'
            }
        self.session = aiohttp.ClientSession(headers=self.headers)


    async def close_session(self):
        if self.session:
            await self.session.close()


def save_html(html):
    with open("good_info.html", 'w') as f:
        f.write(html)
# 目录类，用来表示搜索结果
class Content(AbstractWebPage):
    def __init__(self, cookie, keyword, end_page):
        super(Content, self).__init__(cookie)
        start_url = 'https://www.gwdang.com/search?crc64='
        encoded_keyword = quote(keyword) 
        self.url_list = [start_url + str(j) + '&s_product=' + encoded_keyword + '&site_id=3'for j in range(1, end_page + 1)]
        self.end_page = end_page
        self.PLATFORM = {
            'JD': '3',
            'TM': '83',
            'SN': '25'
        }

    def print(self):
        print(self.url_list, sep='\n')

    async def fetch(self, url):
        async with self.session.get(url) as response:
            response_text = await response.text()
            save_html(response_text)
            return response_text

    async def fetch_all(self):
        tasks = [self.fetch(url) for url in self.url_list]
        return await asyncio.gather(*tasks)

    async def get_item_info_xslx(self):
        wb = openpyxl.load_workbook("/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/good_info2.xlsx")
        ws = wb.active  # 默认获取活动工作表，如果有多个工作表，可以通过 wb[sheet_name] 获取指定工作表

        # 确保表头存在，如果没有表头，添加表头
        if ws.max_row == 1:  # 表格只有一行，说明是新表格，添加表头
            ws.append(["sku", "title", "link", "price", "shop", "img_url"])

        # await self.create_session()
        results = await self.fetch_all()
        # await self.close_session()
        for res in results:
            soup = BeautifulSoup(res, 'html.parser').select('[class="dp-list"]')
            if not soup:
                continue
            good_list = soup[0].select('li')
            print("get good_list", len(good_list))
            for temp in good_list:
                if temp.get('data-dp-id') is None:
                    continue
                sku = temp.get('data-dp-id').strip().split('-')[0]
                good_info = [sku]
                commit_start_url = f'https://item.jd.com/{sku}.html'

                name_div = temp.select_one('[class="item-title"]')
                name = name_div.text.strip()
                good_info.append(name)

                good_info.append(commit_start_url)

                price_div = temp.select_one('[class=bigRedPrice]')
                good_info.append(price_div.text.strip()[1:])

                shop_div = temp.select_one('[class=site]')
                good_info.append(shop_div.get_text().strip())

                img_url = temp.select_one('[class=item-img]').select_one('img').get('data-original')
                good_info.append(img_url)
                
                print(good_info)
                ws.append(good_info)
        print(results)
        wb.save("/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/good_info2.xlsx")

    def get_item_detail_info(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        item_info = {}
        # save_html(html)
        # 获取商品图片
        info_div = soup.select_one('[class=product-info-table]')
        if info_div:
            infos = info_div.select('[class=info-item]')
            for info in infos:
                # print(info)
                key = info.select_one(".info-key").text.replace(":","").strip()
                # print(key)
                value = info.select_one(".info-value").text.strip()
                # print(value)
                item_info[key] = value
        # 获取商品描述
        return item_info

    async def get_detail_string(self, sku=None, platform='JD'):
        if platform in self.PLATFORM:
            platform_str = self.PLATFORM[platform]
        else:
            return None
        item_url = f'https://www.gwdang.com/crc64/dp{sku}-{platform_str}'
        print("in get detail string", item_url)
        async with self.session.get(item_url) as response:
            html = await response.text(encoding='utf-8', errors='ignore')  # 指定编码并忽略错误
            save_html(html)
            item_info = self.get_item_detail_info(html)
            item_info_str = ''
            for key, value in item_info.items():
                item_info_str += key + ':' + value + '\n'
            return item_info_str

async def main():
    cookie_str = ''
    with open('/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/gwdown_cookie.txt') as f:
        cookie_str = f.readline()

    content_page = Content(cookie_str, 'iphone', 1)
    content_page.print()
    await content_page.get_item_info_xslx()
    # string = await  content_page.get_detail_string('100067903671', 'JD')
    await content_page.close_session()
    # print(string)


if __name__ == '__main__':
    asyncio.run(main())