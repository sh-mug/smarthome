import logging
import logging.config
import signal

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

import write_to_db


def on_minute(signum, frame):
    try:
        write_to_db.write_to_influxdb()
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, on_minute)
    signal.setitimer(signal.ITIMER_REAL, 30, 60)

    logger.info('wait for 30 seconds...')

    while True:
        pass
