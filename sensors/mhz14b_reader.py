import datetime
import logging
import sys
import time

import serial
from influxdb import InfluxDBClient

sys.path.append('..')
import config

logger = logging.getLogger(__name__)

co2_sensor_serial = serial.Serial(
    '/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=10.0,
)


def read_co2_data() -> int:
    command_bytes = bytearray(
        [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    co2_sensor_serial.write(command_bytes)
    response = co2_sensor_serial.read(9)

    checksum = -sum(response[1:8]) & 0xFF
    if checksum == response[8]:
        co2_level = int.from_bytes(response[2:4], 'big')
        logger.info(f'{co2_level} ppm')
        return co2_level
    else:
        raise Exception('Checksum did not match')


def write_co2_data_to_influxdb(client: InfluxDBClient, sensor_time: datetime, data: int):
    json_body = [{
        'measurement': 'CO2_LEVEL',
        'tags': {
            'sensor': 'MH-Z14B'
        },
        'time': sensor_time,
        'fields': {
            "value": data
        }
    }]
    client.write_points(json_body)


def main():
    influxdb_client = config.INFLUXDB_CLIENT
    while True:
        sensor_time = datetime.datetime.utcnow()
        co2_data = read_co2_data()
        print(co2_data)
        if sensor_time.second % config.WRITE_INTERVAL == 0:
            write_co2_data_to_influxdb(influxdb_client, sensor_time, co2_data)
        time.sleep(config.MEAUSURE_INTERVAL)


if __name__ == "__main__":
    main()
