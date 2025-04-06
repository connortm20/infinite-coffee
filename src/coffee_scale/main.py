import logging
from logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

from scale import get_stored_readings, save_stored_readings, read_scale
from calculations import update_daily_weights

def main():
    logger.info("starting daily coffee consumption analysis")

    current_scale_reading = read_scale()

    weight_state = get_stored_readings()
    logger.info(f"current weight_tracking_state: {weight_state}")

    new_weight_state = update_daily_weights(weight_state, current_scale_reading)


    save_stored_readings(new_weight_state)

if __name__ == '__main__':
    main()