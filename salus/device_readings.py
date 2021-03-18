class DeviceReadings:
    def __init__(self, data):
        self._current_temperature = float(data.CH1currentRoomTemp)
        self._current_target_temperature = float(data.CH1currentSetPoint)
        self._heat_on = data.CH1heatOnOffStatus == "1"
        self._frost_temperature = float(data.frost)

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def current_target_temperature(self):
        return self._current_target_temperature

    @property
    def heat_on(self):
        return self._heat_on

    @property
    def frost(self):
        return self.frost

