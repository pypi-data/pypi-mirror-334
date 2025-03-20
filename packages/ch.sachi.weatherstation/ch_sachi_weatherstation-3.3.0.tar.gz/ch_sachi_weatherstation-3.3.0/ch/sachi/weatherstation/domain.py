import datetime


class Measure:
    def __init__(self, device_id: int, measured_at: datetime, temperature: float, humidity: float):
        self.device_id = device_id
        self.measured_at = measured_at
        self.temperature = temperature
        self.humidity = humidity

    def to_json(self):
        measured_at_formatted = self.measured_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        return {'measured_at': measured_at_formatted, 'temperature': self.temperature,
                'humidity': self.humidity}
