import json
import logging
logger = logging.getLogger(__name__)

from config import config
EWMA_ALPHA = config['EWMA_ALPHA']
STANDARD_DELIVERY_TIME = config['STANDARD_DELIVERY_TIME']
DEFAULT_COOLDOWN_LENGTH = config['DEFAULT_COOLDOWN_LENGTH']

from scale import get_stored_readings, save_stored_readings

def update_daily_weights(state: dict, new_reading: float) -> dict:
    if state['order_cooldown'] < 0:
        cooldown = state['order_cooldown'] - 1
    else:
        cooldown = 0

    if state['last_reading'] is None:
        return {'emea': 0.0, 'last_reading': new_reading, 'order_cooldown':cooldown}
    
    if state['emea'] == 0.0:
        return {'emea': new_reading - state['last_reading'], 'last_reading': new_reading, 'order_cooldown':cooldown}
                
    delta = new_reading - state['last_reading']

    if delta >= 50: #This is to exclude any large positive changes from affecting the running average. If a new bag of coffee is added we should skip that day's reading from going into the average
        logger.info('Coffee delta exceeded the postive limit and this reading was excluded from the running average')
        emea = state['emea']
    else:
        emea = EWMA_ALPHA * delta + (1 - EWMA_ALPHA) * state['emea'] #Exponetial Weighted Moving Average Calculation

    return {'emea': emea, 'last_reading': new_reading, 'order_cooldown':cooldown}


def is_coffee_needed(current_weight: float, current_emea: float) -> bool:
    '''
        determine if the estimated days before you run out of coffee falls close enough to the configured standard shipping time
    '''
    if current_emea == 0:
        logger.info('Current average rate of change is 0. Prediction dates would be invalid.')
        return False

    if current_emea > 0:
        logger.info('Current coffee daily loss is positive. Predictions for date of zero coffee would not be currently accurate')
        return False

    days_remaining = abs(current_weight / current_emea)
    logger.info(f'Current esimated days of coffee remaining: {days_remaining}')

    if days_remaining <= STANDARD_DELIVERY_TIME:
        return True
    
    return False


def start_order_cooldown(cooldown: int = DEFAULT_COOLDOWN_LENGTH) -> None:
    weight_state = get_stored_readings()

    if weight_state != 0:
        logger.error('order cooldown was started when an existing cooldown should have been respected')

    weight_state['order_cooldown'] = cooldown

    save_stored_readings(weight_state)

    logger.info(f'order cooldown has been set to {cooldown}')

def is_on_order_cooldown() -> bool:
    weight_state = get_stored_readings()
    if weight_state['order_cooldown'] > 0:
         return True
    return False


