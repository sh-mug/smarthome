import datetime

import influxdb

import co2

db = influxdb.InfluxDBClient(
    host='localhost',
    port=8086,
    database='sensor'
)


def write_to_influxdb():
    co2_level = co2.get_co2data_mh_z14b()
    json_body = [{
        'measurement': 'CO2_LEVEL',
        'tags': {
            'sensor': 'MH-Z14B'
        },
        'time': datetime.datetime.utcnow(),
        'fields': {
            "value": co2_level
        }
    }]
    db.write_points(json_body)


if __name__ == '__main__':
    write_to_influxdb()
