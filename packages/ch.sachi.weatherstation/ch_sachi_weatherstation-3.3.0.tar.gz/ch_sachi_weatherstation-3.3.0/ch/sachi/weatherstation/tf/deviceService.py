import datetime
import logging
from os import device_encoding
from typing import List

from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from tinkerforge.ip_connection import IPConnection

from ch.sachi.weatherstation.domain import Measure


class DeviceService:
    def __init__(self, outdoor_weather_uid: str, host: str = 'localhost', port: int = 4223):
        self.uid = outdoor_weather_uid
        self.host = host
        self.port = port

    def get_measures(self) -> List[Measure]:
        ip_connection = self.create_ip_connection()
        ow = self.create_ow_bricklet(ip_connection)

        ip_connection.connect(self.host, self.port)
        try:
            result = []
            device_ids = ow.get_sensor_identifiers()
            for device_id in device_ids:
                device_data = ow.get_sensor_data(device_id)
                if device_data.last_change >= 1200:
                    logging.debug('Measure was done ' + str(device_data.last_change) + 'sec ago, we ignore it')
                    continue
                measured_at = self.get_now() - datetime.timedelta(0, device_data.last_change)
                measure = Measure(device_id, measured_at, device_data.temperature / 10, device_data.humidity)
                result.append(measure)
            return result
        finally:
            ip_connection.disconnect()

    def get_now(self) -> datetime:
        return datetime.datetime.now()

    def create_ow_bricklet(self, ip_connection) -> BrickletOutdoorWeather:
        return BrickletOutdoorWeather(self.uid, ip_connection)

    def create_ip_connection(self) -> IPConnection:
        return IPConnection()
