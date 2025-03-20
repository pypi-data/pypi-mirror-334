import datetime
import logging
import os
import sqlite3
from datetime import timedelta
from sqlite3.dbapi2 import Connection
from typing import List

from ch.sachi.weatherstation.domain import Measure


class MeasureRepository:
    def __init__(self, database: str):
        self.database = database

    def get_devices(self) -> List[int]:
        conn = sqlite3.connect(self.database)
        with conn:
            records = self.__select_and_fetch(conn, 'SELECT distinct(deviceid) from measure')
            device_ids = []
            for record in records:
                device_ids.append(record[0])
            return device_ids

    def get_measures_after(self, device_id: int, last: str) -> List[Measure]:
        conn = sqlite3.connect(self.database)
        with conn:
            records = self.__select_and_fetch(conn, 'SELECT m.created_at, m.temperature, m.humidity ' \
                                                    'from measure m ' \
                                                    'where m.deviceid=? and m.created_at >= datetime(?, \'+1 second\')',
                                              (device_id, last))
            measures_data = []
            for record in records:
                measured_at = record[0]
                measured_at_formatted = self.__measured_at(measured_at)
                measures_data.append(Measure(0, measured_at_formatted, record[1], record[2]))
            return measures_data

    def __measured_at(self, measured_at) -> datetime:
        try:
            return datetime.datetime.strptime(measured_at, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return datetime.datetime.strptime(measured_at, '%Y-%m-%d %H:%M:%S')

    def init(self) -> None:
        is_migration: bool = False
        if os.path.isfile(self.database):
            logging.debug('Database file ' + self.database + 'does exist already')
            conn = sqlite3.connect(self.database)
            with conn:
                records = self.__select_and_fetch(conn,
                                                  'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'sensor\'')
                is_migration = (len(records) > 0)

                if not is_migration:
                    return

        logging.debug('Initialize database ' + self.database)
        conn = sqlite3.connect(self.database)
        with conn:
            if is_migration:
                conn.execute('DROP TABLE sensor')
                conn.execute('ALTER TABLE measure RENAME COLUMN sensorid TO deviceid')

            conn.execute('''CREATE TABLE IF NOT EXISTS measure (
                 id INTEGER PRIMARY KEY,
                 created_at TIMESTAMP NOT NULL,
                 temperature real NOT NULL,
                 humidity real NOT NULL,
                 deviceid INTEGER NOT NULL
                )''')

    def save(self, measure: Measure) -> bool:
        logging.info('Save to database')
        conn = sqlite3.connect(self.database)
        with conn:
            last_measure = self.__get_last_measure(conn, measure.device_id)
            if self.__need_to_persist(last_measure, measure):
                cur = conn.cursor()
                cur.execute('INSERT INTO measure(created_at, temperature, humidity, deviceid) values(?, ?, ?, ?)',
                            (measure.measured_at, measure.temperature, measure.humidity, measure.device_id))
                return cur.rowcount > 0
            return False

    def clean_measures(self):
        logging.info('Cleaning measures older than 60 days')
        conn = sqlite3.connect(self.database)
        sixty_days_ago = datetime.datetime.now() - datetime.timedelta(days=60)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "delete from measure where created_at < '" + sixty_days_ago.strftime('%Y-%m-%d %H:%M:%S.%f') + "'")
            return cur.rowcount

    def __need_to_persist(self, last_measure: datetime, new_measure: Measure) -> bool:
        need_to_persist = new_measure.measured_at >= (last_measure + + timedelta(minutes=1))
        if not need_to_persist:
            logging.info(
                'Measure ' + str(new_measure) + ' will not be persisted, last_measure was at ' + str(last_measure))
        return need_to_persist

    def __get_last_measure(self, conn: Connection, device_id: int) -> datetime:
        cur = conn.cursor()
        cur.execute(
            'SELECT MAX(m.created_at) from measure m where m.deviceid=?', (device_id,)
        )
        result = cur.fetchone()
        if len(result) > 0 and result[0] is not None:
            return self.__measured_at(result[0])
        return datetime.datetime(1970, 1, 1)

    def __select_and_fetch(self, conn, stmt, parameters=()):
        cur = conn.cursor()
        cur.execute(stmt, parameters)
        records = cur.fetchall()
        return records
