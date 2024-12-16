import aiohttp
import asyncio
import os
import time
from bs4 import BeautifulSoup

with open('/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/amazon_cookie.txt','r') as f:
    cookie=f.read()
    
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Host": "www.amazon.com",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "device-memory": "8",
        "sec-ch-device-memory": "8",
        "dpr": "1",
        "sec-ch-dpr": "1",
        "viewport-width": "1287",
        "sec-ch-viewport-width": "1287",
        "rtt": "250",
        "downlink": "10",
        "ect": "4g",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"15.0.0"',
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6",
        "Cookie": cookie,   # 直接从你设置邮编后的亚马逊网页 F12 查看获取
    }
   
    
def get_item_info_dict(html):
    item_list = []  # 用于存储所有商品的字典
    # 定位搜索结果主体，并获取所有的商品的标签
    soup = BeautifulSoup(html, 'html.parser')
    try:
        good_list = soup.select('div.s-main-slot div.s-result-item')
    except:
        print('Skip No items found')
    # 循环获取所有商品信息
    for temp in good_list:
        item_info = {}  # 用于存储单个商品的字典
        
        # sku
        asin = temp.get('data-asin')
        if not asin:
            continue
        item_info['sku'] = asin
        
        # 获取名称信息
        name_div = temp.select_one('div[data-cy="title-recipe"] span')
        if name_div:
            item_info['title'] = name_div.text.strip()
        
        # 商品链接
        item_url = temp.select_one('a.a-link-normal')
        if item_url:
            item_info['link'] = "https://www.amazon.com" + item_url.get('href')
        else:
            continue
        # 价格信息
        price_whole = temp.select_one('span.a-price-whole')
        price_fraction = temp.select_one('span.a-price-fraction')
        if price_whole and price_fraction:
            item_info['price'] = price_whole.text.replace(',','').strip() + price_fraction.text.strip()
        else:
            continue
        
        # 图片信息
        img_div = temp.select_one('img.s-image')
        if img_div:
            item_info['img_url'] = img_div.get('src')
        
        item_info['shop'] = "Amazon"
        item_info['shop_link'] = "https://www.amazon.com"
        # 将商品信息字典加入列表
        item_list.append(item_info)
    # 返回商品字典列表
    return item_list
    
def save_html(content):
    # 确保目录存在
    directory = "page"
    if not os.path.exists(directory):
        os.makedirs(directory)
 
    # 生成文件名
    filename = time.strftime("%Y%m%d%H%M%S") + ".html"
    filepath = os.path.join(directory, filename)
 
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    print("页面已保存至:", filepath)
 
async def monitor_amazon():
    
    # 监控的产品，搜索词
    keyword = "iphone"
    search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
 
    async with aiohttp.ClientSession() as session:
        response = await session.get(search_url, headers=headers)
        html = await response.text()
        await session.close()
        item_list = get_item_info_dict(html)
        # save_html(html)
        if "dogs of amazon" in html.lower():
            print("搜索被标识为异常访问")
        return item_list
        # elif asin.lower() in html.lower():
        #     print("在 Amazon 搜索结果页找到了关键词")
        # else:
        #     print("在 Amazon 搜索结果页未找到 ASIN 关键词，发送警告")
def get_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_whole = soup.select_one('span.a-price-whole')
    price_fraction = soup.select_one('span.a-price-fraction')
    if price_whole and price_fraction:
        return price_whole.text.replace(',','').strip() + price_fraction.text.strip()
    else:
        return None
    
def get_item_detail_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    item_info = {}

    # 获取商品标题
    # title_div = soup.select_one('#productTitle')
    # if title_div:
    #     item_info['title'] = title_div.text.strip()

    # 获取商品价格
    # price_whole = soup.select_one('span.a-price-whole')
    # price_fraction = soup.select_one('span.a-price-fraction')
    # if price_whole and price_fraction:
    #     item_info['price'] = price_whole.text.replace(',','').strip() + price_fraction.text.strip()

    # 获取商品图片
    img_div = soup.select_one('#imgTagWrapperId img')
    if img_div:
        item_info['img_list'] = img_div.get('src')

    # 获取商品描述
    description_div = soup.select_one('#productDescription')
    if description_div:
        item_info['简介'] = description_div.text.strip()

    detail_info1 = soup.select_one('#productFactsDesktopExpander').select('li')
    detail_info2 = soup.select_one('#detailBullets_feature_div').select('li')
    for i in detail_info1 + detail_info2:
        if ':' in i.text:
            key, value = i.text.split(':', 1)  # 只分割一次，避免值中有 ":" 的情况
        item_info[key.replace('\n', '').replace('\u200f', '').strip()] = value.replace('\n', '').replace('\u200e', '').strip()
    
    
    # 获取商品评分
    rating_div = soup.select_one('.reviewCountTextLinkedHistogram')
    if rating_div:
        item_info['评分'] = rating_div.select_one('[class="a-size-base a-color-base"]').text.strip()
        

    # 获取商品评论数
    review_count_div = soup.select_one('#acrCustomerReviewText')
    if review_count_div:
        item_info['评论数'] = review_count_div.text.strip()

    return item_info

async def fetch_item_detail(session, url):
    async with session.get(url, headers=headers) as response:
        html = await response.text()
        save_html(html)
        return get_item_detail_info(html)
    
async def detail():
    item_url = "https://www.amazon.com/zh/dp/B08BWWR15B"  # 替换为实际的商品详情页 URL
    async with aiohttp.ClientSession() as session:
        item_info = await fetch_item_detail(session, item_url)
        return item_info
# 在 Windows 中使用 SelectorEventLoop
if __name__ == '__main__':
    # if os.name == 'nt':
    #     loop = asyncio.SelectorEventLoop()
    #     asyncio.set_event_loop(loop)
    # else:
    #     loop = asyncio.get_event_loop()
 
    # loop.run_until_complete(monitor_amazon())
    # loop.close()
    # item_list = asyncio.run(monitor_amazon())

    # with open('page/20241214160011.html','r') as f:
    #     html=f.read()
    # item_list = get_item_info_dict(html)
    # for item in item_list:
    #     print(item)
    
    item_info = asyncio.run(detail())
    # with open('page/20241214202929.html','r') as f:
    #     html=f.read()
    item_info = get_item_detail_info(item_info)
    print(item_info)