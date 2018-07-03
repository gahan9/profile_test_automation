# coding=utf-8
import logging
import os
import json
import configparser
from datetime import datetime

__author__ = "Gahan Saraiya"


PLATFORM = os.sys.platform
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")
CAPTCHA_DIR = os.path.join(BASE_DIR, "captchas")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
LOG_DIR = os.path.join(BASE_DIR, "logs")
CONFIG_LOCATION = "defaults.config"
CREDENTIAL_JSON = "credential.json"
if PLATFORM == "win32":
    BROWSER_DRIVERS = {
        "chrome": "chromedriver.exe",
        "firefox": "geckodriver.exe"
    }
else:
    os.sys.path.append(BASE_DIR)
    BROWSER_DRIVERS = {
        "chrome": "chromedriver",
        "firefox": "geckodriver"
    }


class Settings(object):
    default_credentials = {
        "username": "demo",
        "password": "demo123"
    }
    default_config_path = "defaults.config"
    logger = logging.getLogger('sms_automation_test')

    def __init__(self):
        for path in [SNAPSHOT_DIR, CAPTCHA_DIR, DOWNLOAD_DIR, LOG_DIR]:
            os.makedirs(path, exist_ok=True)
        self.configure_logger()

    @staticmethod
    def configure_logger():
        logger = logging.getLogger('sms_automation_test')  # create logger with 'sms_automation_test
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(name)-12s] [%(levelname)s]: %(message)s',
                            datefmt='[%Y-%d-%m_%H.%M.%S]',
                            filename=os.path.join(LOG_DIR, 'sms_automation_test_{}.log'.format(datetime.now().strftime('%Y-%d-%m_%H.%M.%S'))),
                            filemode='w')
        # create file handler which logs even debug messages
        # fh = logging.FileHandler('sms_automation_test_{}.log'.format(datetime.now().strftime('%Y-%d-%m_%H.%M.%S')))
        # fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()  # create console handler with a higher log level
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(ch)

    def read_config(self, config_path=None):
        config_path = self.default_config_path if not config_path else config_path
        _config = configparser.RawConfigParser()
        _config.read(config_path)
        return _config

    def read_json(self, json_path=None):
        if not json_path or not os.path.exists(json_path):
            content = self.default_credentials
        else:
            with open(json_path, "r") as f:
                content = json.loads(f.read())
        credentials = content if content else self.default_credentials
        return credentials


settings = Settings()  # settings object
CONFIG = settings.read_config(CONFIG_LOCATION)  # get config
# DOWNLOAD_DIR = CONFIG.get("BROWSER_CONFIG", "DOWNLOAD_DIRECTORY") if os.path.exists(CONFIG.get("BROWSER_CONFIG", "DOWNLOAD_DIRECTORY")) else DOWNLOAD_DIR
CREDENTIALS = settings.read_json(CREDENTIAL_JSON)  # get credentials
BROWSER = CONFIG.get("BROWSER_CONFIG", "BROWSER")  # get defined browser
BROWSER_WIDTH = CONFIG.get("BROWSER_CONFIG", "WIDTH")
BROWSER_HEIGHT = CONFIG.get("BROWSER_CONFIG", "HEIGHT")
BROWSER_DRIVER = BROWSER_DRIVERS.get(BROWSER, None) if BROWSER_DRIVERS.get(BROWSER, None) else BROWSER_DRIVERS["chrome"]  # set chrome as default if invalid browser name
BASE_API_DOMAIN = CONFIG.get("API_CONFIG", "API_DOMAIN")  # API Domain
API_URL = BASE_API_DOMAIN + CONFIG.get("API_CONFIG", "API_PATH")  # API url
settings.logger.info(
        "SYSTEM CONFIGS" +
        "\n\t\t\tBROWSER_DRIVER : " + BROWSER_DRIVER +
        "\n\t\t\tBROWSER_WIDTH : " + BROWSER_WIDTH +
        "\n\t\t\tBROWSER_HEIGHT : " + BROWSER_HEIGHT +
        "\n\t\t\tBASE_DIR : " + BASE_DIR +
        "\n\t\t\tSNAPSHOT_DIR : " + SNAPSHOT_DIR +
        "\n\t\t\tCAPTCHA_DIR : " + CAPTCHA_DIR +
        "\n\t\t\tDOWNLOAD_DIR : " + DOWNLOAD_DIR +
        "\n\t\t\tBASE_API_DOMAIN : " + BASE_API_DOMAIN +
        "\n\t\t\tAPI_URL : " + API_URL +
        "")
