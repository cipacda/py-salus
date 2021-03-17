class Device:
    def __init__(self, device_id, name):
        self._id = device_id
        self._name = name

    @property
    def device_id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return self._id == other.device_id and self._name == other.name

    @staticmethod
    def create_from_html(html):
        return Device(
            html.find("input", {"name": "devId"})['value'],
            html.find("a", {"class": "deviceIcon"}).text,
        )
