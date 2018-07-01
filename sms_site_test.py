# coding=utf-8
import time
import base64
import requests
import unittest
from datetime import datetime

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# imports for cropping snapshot
from PIL import Image
from io import BytesIO

# imports constants
from configure import *

__author__ = "Gahan Saraiya"


def _sleep(seconds=2, flag=True):
    if flag:
        time.sleep(seconds)


class BaseTest(unittest.TestCase):
    live_server_url = "http://urbanprofile.gujarat.gov.in/"
    chrome_driver_path = BROWSER_DRIVER
    credentials = CREDENTIALS
    scroll_pause_time = 0.5

    def setUp(self):
        if BROWSER is "chrome":
            self.opts = webdriver.ChromeOptions()
            self.opts.add_experimental_option("detach", True)
            self.opts.add_argument("--disable-extensions")
            self.selenium = webdriver.Chrome(self.chrome_driver_path, options=self.opts)
        else:
            self.opts = webdriver.FirefoxOptions()
            self.opts.add_argument("--detach")
            self.selenium = webdriver.Firefox()

    def tearDown(self):
        pass
        # self.selenium.close()
        # super().tearDownClass()

    @staticmethod
    def crop_image(img_element, snapshot):
        location, size = img_element.location, img_element.size

        img = Image.open(BytesIO(snapshot))
        # im = Image.open(StringIO(base64.decodebytes(self.selenium.get_screenshot_as_base64())))
        left, top = location['x'], location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        img = img.crop((left, top, right, bottom))
        return img

    @staticmethod
    def read_image(img):
        img.save("captcha.png")
        with open("captcha.png", 'rb') as f:
            captcha_content = f.read()
        img_post_data = "data:image/png;base64," + str(base64.b64encode(captcha_content))[2:-1]
        print(API_URL)
        resp = requests.post(API_URL, data={"image": img_post_data})
        print("TEXT-CAPTCHA>>", resp.json().get("text"))
        captcha = resp.json().get('text').strip()
        return captcha

    def _test_login(self):
        self.selenium.get(self.live_server_url)
        username_input = self.selenium.find_element_by_name("txt_user")
        username_input.send_keys(self.credentials['username'])
        password_input = self.selenium.find_element_by_name("txt_pwd")
        password_input.send_keys(self.credentials['password'])
        captcha_input = self.selenium.find_element_by_id("txtturing")
        # workout for captcha
        png = self.selenium.get_screenshot_as_png()
        img = self.selenium.find_element_by_id("Image1")
        im = self.crop_image(img, png)
        captcha = self.read_image(im)
        captcha_input.send_keys(captcha)
        _sleep(1)
        self.selenium.find_element_by_id('btn_login').click()

    def scroll(self):
        # Get scroll height
        last_height = self.selenium.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(self.scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.selenium.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def take_snapshot(self, session_prefix=None):
        now = datetime.now()
        now_date = now.strftime('%d_%b_%Y')
        session_prefix = now.strftime('%Y-%d-%m_%H') if not session_prefix else session_prefix
        _name = "screen-shot_{}.png".format(now.strftime('%Y-%d-%m_%H.%M.%S'))
        _path = os.path.join(SNAPSHOT_DIR, 'selenium', now_date, session_prefix)
        os.makedirs(_path, exist_ok=True)
        self.selenium.save_screenshot(os.path.join(_path, _name))
        print("Snapshot for url : {} saved at: {}".format(self.selenium.current_url, _path))

    class Meta:
        abstract = True


class UrbanProfileTest(BaseTest):
    def _test_town_directory(self):
        element = self.selenium.find_element_by_xpath("//*[contains(text(), 'TOWN DIRECTORY')]")
        element.click()
        _sleep(3)
        table = self.selenium.find_element_by_id("Table2")

    def test_ordered(self):
        self.selenium.set_window_size('1366', '768')
        # self.selenium.fullscreen_window()
        # self.take_snapshot()
        _sleep(1)
        self._test_login()
        _sleep(1)
        self._test_town_directory()
        _sleep(1)


class VillageProfileTest(BaseTest):
    live_server_url = "http://villageprofile.gujarat.gov.in/"

    def _test_login(self):
        self.selenium.get(self.live_server_url)
        username_input = self.selenium.find_element_by_id("LoginUser_UserName")
        username_input.send_keys(self.credentials['username'])
        password_input = self.selenium.find_element_by_id("LoginUser_Password")
        password_input.send_keys(self.credentials['password'])
        captcha_input = self.selenium.find_element_by_id("txtcaptcha")
        # workout for captcha
        png = self.selenium.get_screenshot_as_png()
        img = self.selenium.find_element_by_id("Image1")
        im = self.crop_image(img, png)
        captcha = self.read_image(im)
        captcha_input.send_keys(captcha)
        _sleep(1)
        self.selenium.find_element_by_id('LoginButton').click()

    def test_ordered(self):
        self.selenium.set_window_size('1366', '768')
        _sleep(1)
        self._test_login()


if __name__ == "__main__":
    # unittest.main()
    pass
