import logging

from ch.sachi.weatherstation.logging import configure_logging
from ch.sachi.weatherstation.measureRepository import MeasureRepository
from ch.sachi.weatherstation.tf.deviceService import DeviceService
from .config import *


class Main:
    def __init__(self, device_service: DeviceService, repo: MeasureRepository):
        self.device_service = device_service
        self.repo = repo

    def run(self) -> None:
        logging.debug('Start getting measures')
        measures = self.device_service.get_measures()
        for measure in measures:
            self.repo.save(measure)
        logging.debug('Handled ' + str(len(measures)) + ' measures')


def main():
    config = read_configuration()
    configure_logging(config.loglevel)
    device_service = DeviceService(config.broker.outdoor_weather_uid)
    repo = MeasureRepository(config.database)
    repo.init()
    Main(device_service, repo).run()


if __name__ == '__main__':
    main()
