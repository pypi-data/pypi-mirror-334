import datetime
import logging

from ch.sachi.weatherstation.logging import configure_logging
from ch.sachi.weatherstation.measureRepository import MeasureRepository
from ch.sachi.weatherstation.restServiceMeasures import RestServiceMeasures, RestServiceException
from .config import *


class Main:
    def __init__(self,
                 service: RestServiceMeasures,
                 repo: MeasureRepository):
        self.service = service
        self.repo = repo

    def run(self) -> None:
        start = datetime.datetime.now()
        try:
            posted_measures = 0
            devices = self.repo.get_devices()
            for device_id in devices:
                logging.info('Posting for ' + str(device_id))
                try:
                    last = self.service.get_last_timestamp(device_id)
                except RestServiceException as exception:
                    logging.error('Was not able to get last measure: ' + str(exception))
                    continue
                logging.info('Just look at measures after: ' + str(last))
                measures_to_post = self.repo.get_measures_after(device_id, last)
                measures_per_device = len(measures_to_post)
                logging.info('Trying to post ' + str(measures_per_device) + ' measures')
                if measures_per_device > 0:
                    logging.info('Posting ' + str(measures_per_device) + " for device '" + str(device_id) + "'")
                    try:
                        self.service.post_measures(device_id, measures_to_post)
                        posted_measures += measures_per_device
                    except Exception as postEx:
                        logging.error("Error occurred when posting measures for " + str(device_id) + ": " + str(postEx))
            elapsed_time = datetime.datetime.now() - start
            logging.info('Posted ' + str(posted_measures) + ' in ' + str(elapsed_time))
            deleted_measures = self.repo.clean_measures()
            logging.info('Cleaned ' + str(deleted_measures) + ' in database')
        except Exception as e:
            logging.error("Error occurred: " + str(e))


def main():
    config = read_configuration()
    configure_logging(config.loglevel)
    service = RestServiceMeasures(config.rest.url, config.rest.username, config.rest.password)
    repo = MeasureRepository(config.database)
    Main(service, repo).run()


if __name__ == '__main__':
    main()
