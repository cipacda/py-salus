import os
import unittest
import requests_mock

from salus.api import URL_LOGIN_API, DEVICES_URL
from salus.api import Api
from salus.device import Device

TOKEN_VALUE = "12345-1512904488"
DEVICE_NAME = "STA000123456 Device Name"
DEVICE_ID = "12345678"
VALID_USERNAME = "test@example.com"
VALID_PASSWORD = "password"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(path) as fptr:
        return fptr.read()


def _setup_responses(mock):
    mock.register_uri(
        "POST",
        URL_LOGIN_API,
        text=URL_LOGIN_API,
    )

    mock.register_uri(
        "GET",
        DEVICES_URL,
        text=load_fixture("devices_response.html"),
    )

    mock.register_uri(
        "GET",
        Api.readings_url(DEVICE_ID, TOKEN_VALUE),
        text=load_fixture("device_readings.json"),
    )


class TestApi(unittest.TestCase):
    def test_raises_exception_with_invalid_email(self):
        self.assertRaises(Exception, lambda: Api("test", VALID_PASSWORD))

    def test_raises_exception_with_invalid_password(self):
        self.assertRaises(Exception, lambda: Api(VALID_USERNAME, "invalidPassword"))

    @requests_mock.Mocker()
    def test_can_get_token(self, mock):
        _setup_responses(mock)
        api = Api(VALID_USERNAME, VALID_PASSWORD)
        token = api.get_token_from_api()
        print(token)
        self.assertEqual(token, TOKEN_VALUE)

    @requests_mock.Mocker()
    def test_can_get_devices(self, mock):
        _setup_responses(mock)
        api = Api(VALID_USERNAME, VALID_PASSWORD)
        devices = api.get_devices()
        self.assertListEqual(devices, [Device(DEVICE_ID, DEVICE_NAME)])

    @requests_mock.Mocker()
    def test_reads_device_data(self, mock):
        _setup_responses(mock)
        api = Api(VALID_USERNAME, VALID_PASSWORD)
        readings = api.get_device_reading(DEVICE_ID)
        self.assertEqual(23.5, readings.current_temperature)
        self.assertEqual(24.5, readings.current_target_temperature)
        self.assertEqual(True, readings.heat_on)
        self.assertEqual(9, readings._frost_temperature)
