import os
import json
import configparser


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_DIR = os.path.join(BASE_DIR, "snapshots")
CAPTCHA_DIR = os.path.join(BASE_DIR, "captchas")
CONFIG_LOCATION = "defaults.config"
CREDENTIAL_JSON = "credential.json"
BROWSER_DRIVERS = {
    "chrome": "chromedriver.exe",
    "firefox": "geckodriver.exe"
}


class Settings(object):
    default_credentials = {
        "username": "demo",
        "password": "demo123"
    }
    default_config_path = "defaults.config"

    def __init__(self):
        for path in [SNAPSHOT_DIR, CAPTCHA_DIR]:
            os.makedirs(path, exist_ok=True)

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
CREDENTIALS = settings.read_json(CREDENTIAL_JSON)  # get credentials
BROWSER_DRIVER = BROWSER_DRIVERS.get(CONFIG.get("BROWSER_CONFIG", "BROWSER"), "chromedriver.exe")  # set chrome as default if invalid browser name
BASE_API_DOMAIN = CONFIG.get("API_CONFIG", "API_DOMAIN")  # API Domain
API_URL = BASE_API_DOMAIN + CONFIG.get("API_CONFIG", "API_PATH")  # API url
