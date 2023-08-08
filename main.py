import datetime
import logging
import logging.config
import time

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

import config
from actions import *
from sensors import *


def main():
    influxdb_client = config.INFLUXDB_CLIENT
    high_co2_notified = False

    try:
        while True:
            sensor_time = datetime.datetime.utcnow()

            # Read sensor data
            environment_data = read_environment_data()
            co2_data = read_co2_data()

            # Write sensor data to InfluxDB
            if sensor_time.second % config.WRITE_INTERVAL == 0:
                write_environment_data_to_influxdb(
                    influxdb_client, sensor_time, environment_data)
                write_co2_data_to_influxdb(
                    influxdb_client, sensor_time, co2_data)

            # Perform actions based on sensor data
            if co2_data > config.CO2_THRESHOLD and not high_co2_notified:
                control_led('high_co2')
                send_discord_notification('High CO2 detected!')
                high_co2_notified = True
            if co2_data <= config.CO2_THRESHOLD:
                control_led('normal')
                high_co2_notified = False

            # Wait for the next second
            sleep_time = 1 - (datetime.datetime.utcnow() -
                              sensor_time).total_seconds()
            if sleep_time > 0:
                time.sleep(sleep_time)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
