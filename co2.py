import logging
import time

import serial

logger = logging.getLogger(__name__)

ser = serial.Serial(
    '/dev/ttyS0',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=10.0,
)


def get_co2data_mh_z14b() -> int:
    b = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    ser.write(b)
    result = ser.read(9)

    checksum = -sum(result[1:8]) & 0xFF
    if checksum == result[8]:
        co2_value = int.from_bytes(result[2:4], 'big')
        logger.info(f'{co2_value} ppm')
        return co2_value
    else:
        raise Exception('checksum did not match')


if __name__ == '__main__':
    get_co2data_mh_z14b()
