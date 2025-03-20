import json
import os
import requests
from selenium import webdriver
from loguru import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumSession:
    driver = None
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    def __init__(self, selenium_init_url="https://cn.bing.com", driver_type="firefox", headers=None):
        self.init_headers(headers)
        self.init_driver(driver_type)
        self.selenium_get(selenium_init_url)

    def init_headers(self, headers):
        logger.debug("初始化请求头中...")
        if headers is not None:
            self.headers.update(headers)

    def init_driver(self, driver_type):
        match driver_type:
            case "firefox":
                logger.debug("加载浏览器firefox...")
                self.driver = webdriver.Firefox()
            case "chrome":
                logger.debug("加载浏览器chrome...")
                self.driver = webdriver.Chrome()
            case "edge":
                logger.debug("加载浏览器edge...")
                self.driver = webdriver.Edge()
            case _:
                logger.debug("加载浏览器firefox...")
                self.driver = webdriver.Firefox()

    def get(self, url, **kwargs):
        logger.debug(f"session请求(method: GET): {url}")
        res = self.session.get(url, **kwargs)
        self.cookies_to_driver()
        return res

    def post(self, url, data=None, json=None, **kwargs):
        logger.debug(f"session请求(method: POST): {url}")
        res = self.session.post(url, data=data, json=json, **kwargs)
        self.cookies_to_driver()
        return res

    def request(self, url, method, **kwargs):
        logger.debug(f"session请求(method: {method}): {url}")
        res = self.session.request(method=method, url=url, **kwargs)
        self.cookies_to_driver()
        return res

    def get_session_cookies_to_dict(self):
        cookies = self.session.cookies.get_dict()
        selenium_cookies = []
        for k, v in cookies.items():
            selenium_cookies.append({
                "name": k,
                "value": v,
            })
        return selenium_cookies

    def cookies_to_driver(self):
        for i in self.get_session_cookies_to_dict():
            self.driver.add_cookie(i)
        self.driver.refresh()

    def selenium_get(self, url):
        logger.debug(f"浏览器请求: {url}")
        self.driver.get(url)
        self.selenium_cookies_to_session()
        self.driver.implicitly_wait(60)

    def selenium_cookies_to_session(self):
        for cookie in self.driver.get_cookies():
            self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"], path=cookie["path"])

    def send_key(self, value, send_value, by=By.CSS_SELECTOR, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        ).send_keys(send_value)

    def click(self, value, by=By.CSS_SELECTOR, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        ).click()

    def hover(self, value, by=By.CSS_SELECTOR, timeout=60):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        ActionChains(self.driver).move_to_element(element).perform()

    @staticmethod
    def on_input(des=""):
        return input(des)

    def scroll(self, height=200):
        self.driver.execute_script("window.scrollTo(0, {})".format(height))

    def scroll_to_el(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def scroll_to_el_by_value(self, value, by=By.CSS_SELECTOR):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(by, value))

    def scroll_to_top(self):
        self.driver.execute_script("var q=document.documentElement.scrollTop=0")

    def scroll_to_bottom_fade(self):
        """
        平滑滑动
        :return:
        """
        for i in range(10):
            self.scroll((i + 1) * 1000)

    def scroll_to_bottom(self):
        """
        直接到达底部
        :return:
        """
        self.driver.execute_script("var q=document.documentElement.scrollTop=10000")

    def save_cookies(self, save_path):
        logger.info(f"正在保存cookie中...")
        with open(save_path, "w") as f:
            f.write(json.dumps(self.driver.get_cookies()))

    def load_cookies(self, load_path):
        if os.path.exists(load_path):
            logger.info(f"找到{load_path}, 正在加载cookie中...")
            with open(load_path, "r") as f:
                cookies = json.loads(f.read())
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                    self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"],
                                             path=cookie["path"])
                self.driver.refresh()


