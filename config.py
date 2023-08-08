from influxdb import InfluxDBClient

INFLUXDB_CLIENT = InfluxDBClient(
    host='localhost',
    port=8086,
    database='sensor'
)

MEAUSURE_INTERVAL = 1
WRITE_INTERVAL = 15

CO2_THRESHOLD = 1000
