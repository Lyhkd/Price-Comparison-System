# 京东定向爬取搜索信息
import requests
from bs4 import BeautifulSoup
import time
import re
# 获取URL页面
def getHTMLText(url, code='utf-8'):
    head = {
        'referer': 'https://search.jd.com/',  # 每个页面的后半部分数据，是通过下拉然后再次请求，会做来源检查。
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': 'retina=1; cid=9; appCode=ms0ca95114; webp=1; __jdv=122270672%7Cdirect%7C-%7Cnone%7C-%7C1730879043820; mba_muid=1730879043820508003444; 3AB9D23F7A4B3C9B=HCA3Y6EQYEEX4D3CSBC776NU4BWJO6D43D2K3NCG643VSEJJQSIZLNS74EUCGFOLDOY6JUUTXFUEDPRGB5DWYWGLW4; visitkey=4761193564436579369; shshshfpa=16da7eda-c753-8aea-d274-ea2d3a478eac-1730879058; shshshfpx=16da7eda-c753-8aea-d274-ea2d3a478eac-1730879058; jcap_dvzw_fp=dDdDjvj8ufN4dPmb3P0jmXmye5L-XME9oYGPxor_Fya9nwsS5hIT0O1RgttwaMdNLmE1XO9b_LSid7nIEczBDQ==; whwswswws=; sc_width=1280; wxa_level=1; jxsid=17310496622724447403; cd_eid=jdd03HCA3Y6EQYEEX4D3CSBC776NU4BWJO6D43D2K3NCG643VSEJJQSIZLNS74EUCGFOLDOY6JUUTXFUEDPRGB5DWYWGLW4AAAAMTABXDYGIAAAAADQA5OJ5QHG5DCIX; share_cpin=; share_open_id=; share_gpin=; shareChannel=; source_module=; erp=; mt_xid=V2_52007VwMUUFxRVFIeTBtVBmYHE1tcWVBfGkwpDgNgCkABVQtOCE0eSkAAY1QTTg5bB1kDGhpeVjcAF1JbXFFbL0oYXwB7AxJOXFFDWhtCGVoOZwAiUG1YYlgYTRtdAmADFFdaaFJTGEk%3D; warehistory="100123251383,"; PPRD_P=UUID.1730879043820508003444-LOGID.1731050233085.1135744024; __jda=26066735.1730879043820508003444.1730879043.1730879043.1731049662.2; __jdc=26066735; __jdu=1730879043820508003444; 3AB9D23F7A4B3CSS=jdd03HCA3Y6EQYEEX4D3CSBC776NU4BWJO6D43D2K3NCG643VSEJJQSIZLNS74EUCGFOLDOY6JUUTXFUEDPRGB5DWYWGLW4AAAAMTBKZ3QWQAAAAACZEOK7WB2IZKGUX; _gia_d=1; __wga=1731051374230.1731049668881.1730879134460.1730879134460.14.2; jxsid_s_u=https%3A//my.m.jd.com/account/index.html; jxsid_s_t=1731051374304; shshshfpb=BApXS85a9CfZALNDKNRRkXmC9g1qBgT92BnLGl3dp9xJ1Mu8lNoG2; TrackerID=cBDgLZ7GC7ztu-AQnEBdj98fFtLHosGHrFGhfvCxNQMdMRWP5ez869BSJo6O8E-2awmPFldqR8AeWfIkkp_UPS79cKPrc276_v6DC56NH6eBcXRlbqXFCqayZpTtAlel; pt_key=AAJnLb_VADBDJWXb769etsCcbyHq-GKw_x5S_bJsDa9rkj6qWtTlDKMC8SsI33GSBUJRVX7EbVI; pt_pin=jd_4ed2d819a8d78; pt_token=1dulqemy; pwdt_id=jd_4ed2d819a8d78; sfstoken=tk01maf8d1cc7a8sM3gxeDJ4M2tHJhnVU/pmWWRKCyJHNVfhiBoEvc3k94aQjSyG4R0agIfkj7okwjBxAitRRKmiFjLk; wqmnx1=MDEyNjM4Ny9tMTZvLm5uIF9waTYsZXIuYTczN2E1V0RVKQ%3D%3D; __jdb=26066735.40.1730879043820508003444|2.1731049662; mba_sid=17310496623154114952382905785.47; __jd_ref_cls=MSearch_DarkLines'
    }
    try:
        r = requests.get(url, timeout=30, headers=head)
        r.raise_for_status()
        r.encoding = code
        print(r.text)
        return r.text
    except:
        return "获取URL页面失败"
# 解析html信息
def parsePage(ilt, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        nameInfo = soup.find_all('div', attrs={'class': 'p-name'})
        priceInfo = soup.find_all('div', attrs={'class': 'p-price'})
        # print(nameInfo)
        # print(priceInfo)
        for i in range(len(nameInfo)):
            titlelst = nameInfo[i].find('em').text.split()
            name = ""
            for j in range(len(titlelst)):  # 此处要注意循环变量不能混淆，与JS不同
                # 注意！！！此处之前是选择了截取长度，但是截取长度导致了后几个页面有些数据丢失，不知道为什么 :TODO
                name = name + titlelst[j] + " "
            price = priceInfo[i].find('strong').text
            if (price == '￥'):  # 特殊情况，特殊处理
                price = '￥' + priceInfo[i].find('strong')['data-price']
            ilt.append([price, name])
    except:
        print("解析HTML内容失败")
# 打印商品信息
def printGoodList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))
# 主函数
def main():
    pages = input("请输入要爬取的页数 ")
    goods = '手机'
    depth = eval(pages)
    timeID = '%.5f' % time.time()  # 时间戳保留后五位
    # print(timeID)
    for i in range(depth):
        try:
            print("以下是第 ------ %d ------ 页数据" % (i + 1))
            info_list = []
            url = 'https://search.jd.com/Search?keyword=' + goods + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + goods + '&cid2=653&cid3=655&page=' + str(
                (i + 1) * 2 - 1) + '&click=0'  # 此处注意 应该给i加1，注意细节
            html = getHTMLText(url)
            parsePage(info_list, html)
            url = 'https://search.jd.com/s_new.php?keyword=' + goods + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + goods + '&cid2=653&cid3=655&page=' + str(
                (i + 1) * 2) + '&scrolling=y&log_id=' + str(timeID) + '&tpl=3_M'
            html = getHTMLText(url)
            parsePage(info_list, html)
            printGoodList(info_list)
            time.sleep(1)  # 提升视觉效果
        except:
            continue
main()
