import json
import logging
import platform
import sys
from typing import List

import requests
from importlib_metadata import version

from ch.sachi.weatherstation.domain import Measure


class RestServiceMeasures:
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.auth = {'username': username, 'password': password}
        hm_version = version('ch.sachi.weatherstation')
        user_agent = 'python(' + platform.python_version() + ')/weatherstation(' + hm_version + ')'
        self.headers = {'User-Agent': user_agent}
        self.login()

    def login(self) -> None:
        logging.debug("Try to login to " + self.url + '/login')
        try:
            response = requests.post(self.url + '/login', data=json.dumps(self.auth), headers=self.headers, timeout=20)
        except requests.exceptions.RequestException as e:
            logging.exception("RequestException occured: " + str(e))
            sys.exit(1)

        if not response.ok:
            response.raise_for_status()
        str_response = response.content.decode('utf-8')
        logging.debug(str_response)
        if str_response:
            jwt_data = json.loads(str_response)
            jwt = jwt_data['access_jwt']
            logging.info(jwt)
            self.headers['Authorization'] = 'Bearer ' + jwt

    def get_last_timestamp(self, device_id: int) -> str:
        response = requests.get(self.url + '/devices/' + str(device_id) + '/measures/last', headers=self.headers,
                                timeout=10)
        if response.ok:
            str_response = response.content.decode('utf-8')
            logging.debug(str_response)
            if str_response:
                last = json.loads(str_response)
                return last['measured_at']
            return '1970-01-01 00:00'
        else:
            raise RestServiceException('Not found')

    def post_measures(self, device_id: int, measures: List[Measure]) -> None:
        measures_data = []
        for measure in measures:
            data = measure.to_json()
            measures_data.append(data)
        logging.debug('Headers:')
        logging.debug(self.headers)
        response = requests.post(self.url + '/devices/' + str(device_id) + '/measures', data=json.dumps(measures_data), headers=self.headers,
                                 timeout=120)
        logging.debug(response)
        if not response.ok:
            response.raise_for_status()


class RestServiceException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
