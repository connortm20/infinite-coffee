import logging
import sys

from scale import get_stored_readings, save_stored_readings, read_scale
from calculations import update_daily_weights, is_coffee_needed
from messaging import send_message
from logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) == 2:
        current_scale_reading = float(sys.argv[1])
        logger.debug(f'weight reading from incoming argv saved as {current_scale_reading}')
    else:
        current_scale_reading = read_scale()
        logger.debug(f'weight reading from default function saved as {current_scale_reading}')

    logger.info("starting daily coffee consumption analysis")

    weight_state = get_stored_readings()
    logger.debug(f"current weight_tracking_state: {weight_state}")

    new_weight_state = update_daily_weights(weight_state, current_scale_reading)

    save_stored_readings(new_weight_state)

    if is_coffee_needed(current_scale_reading, new_weight_state['emea']):
        print('TIME TO ORDER COFFEE')


if __name__ == '__main__':
    main()