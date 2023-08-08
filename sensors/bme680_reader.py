import datetime
import logging
import sys
import time

import bme680
from influxdb import InfluxDBClient

sys.path.append('..')
import config

logger = logging.getLogger(__name__)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)


def read_environment_data() -> dict:
    if sensor.get_sensor_data():
        temperature = sensor.data.temperature
        pressure = sensor.data.pressure
        humidity = sensor.data.humidity
        logger.info(
            f'{temperature:.2f} C, {pressure:.2f} hPa, {humidity:.2f} %RH')
        return {
            'temperature': temperature,
            'pressure': pressure,
            'humidity': humidity
        }
    else:
        raise Exception('Failed to read environment data')


def write_environment_data_to_influxdb(client: InfluxDBClient, sensor_time: datetime, data: dict):
    json_body = [{
        'measurement': 'ENVIRONMENT',
        'tags': {
            'sensor': 'BME680'
        },
        'time': sensor_time,
        'fields': data
    }]
    client.write_points(json_body)


def main():
    influxdb_client = config.INFLUXDB_CLIENT
    while True:
        sensor_time = datetime.datetime.utcnow()
        environment_data = read_environment_data()
        print(environment_data)
        if sensor_time.second % config.WRITE_INTERVAL == 0:
            write_environment_data_to_influxdb(
                influxdb_client, sensor_time, environment_data)
        time.sleep(config.MEAUSURE_INTERVAL)


if __name__ == "__main__":
    main()
