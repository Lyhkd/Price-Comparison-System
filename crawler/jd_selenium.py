from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def load_cookies_from_file(file_path):
    cookies = []
    with open(file_path, 'r') as f:
        cookie_str = f.read().strip()
        for cookie in cookie_str.split(';'):
            name, value = cookie.split('=', 1)
            cookies.append({"name": name.strip(), "value": value.strip()})
    return cookies

def add_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
        
def setup_driver():
    print("set up driver")
    # 设置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'none'
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # 设置 ChromeDriver 路径
    service = Service('/opt/homebrew/bin/chromedriver')  # 替换为你的 ChromeDriver 路径

    # 初始化 WebDriver
    print("driver set up")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("driver set up")
    return driver

def scrape_jd_product_data(sku=None):
    driver = setup_driver()
    print("show window")
    # driver.maximize_window()
    sku = 100149996442
    url = f'https://item.jd.com/{sku}.html'
    driver.get(url)
    # 读取并设置 Cookie
    cookies = load_cookies_from_file('/Users/lyhkd/ZJU/Fall2024/BS/Price-Comparison-System/crawler/cookie.txt')
    add_cookies(driver, cookies)
    # 刷新页面以应用 Cookie
    print("refresh page")
    driver.refresh()
    
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # 等待页面加载
    # 等待页面加载完成
    print("waiting for page to load")
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
        
        
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "p-price"))
    )
    price_element = driver.find_element(By.CLASS_NAME, "p-price")
    elements = price_element.find_elements(By.TAG_NAME, "span")
    price_value = []
    for item in elements:
        price_value.append(item.text)
        print(item.text)
        
    product_data = {
        "price": price_value
    }
    
    print(price_element)
    print(price_value)
    

    driver.quit()
    return product_data

if __name__ == "__main__":
    data = scrape_jd_product_data()
    print(data)