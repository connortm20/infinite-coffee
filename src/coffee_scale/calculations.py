EWMA_ALPHA = .5 #alpha parameter for EWEA i.e. smoothing

def update_daily_weights(state: dict, new_reading: float) -> dict:
    if state['last_reading'] is None:
        return {'emea': 0.0, 'last_reading': new_reading}
        
    delta = new_reading - state['last_reading']
    emea = EWMA_ALPHA * delta + (1 - EWMA_ALPHA) * state['emea'] #Exponetial Weighted Moving Average Calculation
    return {'emea': emea, 'last_reading': new_reading}

