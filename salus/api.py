import requests
import json
from types import SimpleNamespace
from bs4 import BeautifulSoup
from cachetools import TTLCache
from salus.device import Device
from salus.device_readings import DeviceReadings

BASE_URL = "https://salus-it500.com/"
URL_LOGIN_API = f"{BASE_URL}public/login.php"
DEVICES_URL = f"{BASE_URL}public/devices.php"

LOGIN_PAGE_TEXT = "loginRegister"
INVALID_LOGIN_TEXT = "Invalid login name or password"
INVALID_EMAIL_TEXT = "Please enter a valid email address."

class Api:
    def __init__(self, username, password):
        self._username = username
        self._password = password

        self._session = requests.Session()

        self._cache = TTLCache(maxsize=10, ttl=5*60*1000)

        self.login()

    def login(self):
        response = self._session.post(URL_LOGIN_API, {
            "IDemail": self._username,
            "password": self._password,
            "login": "Login",
        })

        response_text = response.text

        if response_text.find(INVALID_LOGIN_TEXT) != -1 or response_text.find(INVALID_EMAIL_TEXT) != -1:
            raise Exception("Invalid credentials")

    def get_token_from_api(self):
        self.login()
        devices_list = self._session.get(DEVICES_URL).text
        soup = BeautifulSoup(devices_list, "html.parser")

        token = soup.find("input", {"name": "token"})['value']
        self._cache['token'] = token
        print(f"Loaded token {token}")
        return token

    def get_token(self):
        if self._cache.get("token"):
            return self._cache.get("token")

        return self.get_token_from_api()

    def get_devices(self):
        def request(): return self._session.get(DEVICES_URL).text
        devices_list = self.make_request(request)
        soup = BeautifulSoup(devices_list, "html.parser")

        all_devices_html = soup.select("div.deviceList:has(> a.deviceIcon)")
        return [Device.create_from_html(d) for d in all_devices_html]

    def get_device_reading(self, device_id):
        token = self.get_token()
        url = self.readings_url(device_id, token)
        print(url)
        readings_data = requests.get(url).text
        response = json.loads(readings_data, object_hook=lambda d: SimpleNamespace(**d))
        return DeviceReadings(response)

    def make_request(self, method):
        response = method()
        if response.find(LOGIN_PAGE_TEXT):
            self.login()
            self._token = self.get_token()
            response = method()

        return response

    @staticmethod
    def readings_url(device_id, token):
        return f"{BASE_URL}/public/ajax_device_values.php?devId={device_id}&token={token}"
