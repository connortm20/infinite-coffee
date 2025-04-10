import logging

logger = logging.getLogger(__name__)


EWMA_ALPHA = .5 #alpha parameter for EWEA i.e. smoothing. Value 0 - 1. Larger values correlate to newer values affecting the average by a greater degree
STANDARD_DELIVERY_TIME = 5 #time in days estimate for coffee to go from order to doorstep

def update_daily_weights(state: dict, new_reading: float) -> dict:
    if state['last_reading'] is None:
        return {'emea': 0.0, 'last_reading': new_reading}
        
    delta = new_reading - state['last_reading']
    emea = EWMA_ALPHA * delta + (1 - EWMA_ALPHA) * state['emea'] #Exponetial Weighted Moving Average Calculation
    return {'emea': emea, 'last_reading': new_reading}


def is_coffee_needed(current_weight: float, current_emea: float) -> bool:
    '''
        determine if the estimated days before you run out of coffee falls close enough to the configured standard shipping time
    '''
    if current_emea > 0:
        logger.info('current coffee daily loss is positive. Predictions for date of zero coffee would not be currently accurate')
        return False

    days_remaining = abs(current_weight / current_emea)
    logger.info(f'Current esimated days of coffee remaining: {days_remaining}')

    if days_remaining <= STANDARD_DELIVERY_TIME:
        return True
    
    return False
