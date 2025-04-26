import json
from pathlib import Path
import logging
from serial import Serial
import time

logger = logging.getLogger(__name__)

PERSISTENT_DATA_FILE = Path('weight.json')

def init_scale(port : str, init_delay = 10) -> Serial:
    '''
    perform and setup or initialization to read from the scale board
    '''
    ser = Serial(port, 9600, timeout=1)  
    time.sleep(init_delay) 
    ser.reset_input_buffer()

    return ser
    

def read_scale(max_attempts:int=10, retry_delay:int=1) -> float:
    '''
    attempts to read from serial input and convert reading to grams
    '''
    ser = init_scale('COM3')

    if ser is None:
        logger.error("no serial stream initialized. Unable to read scale data")
        raise

    try:
        for attempt in range(1, max_attempts+1):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            logger.debug(f'raw scale line read: "{line}" on read attempt {attempt}')
        
            if line and len(line) > 0:
                break

            time.sleep(retry_delay)

        weight, unit, temp, _ = line.split(',')
        logger.info('scale reading : "{weight}" with unit : "{unit}"')

        if unit != 'kg':
            logger.error(f'unit reading from serial did not match expected "kg". unit: {unit}')
            raise

        weight_in_grams = round(100 * float(weight), 2)
        return weight_in_grams


    except ValueError as e:
        logger.error("could not parse scale data (%r): %s", line, e)
        raise

    except Exception as e:
        logger.exception(f"unexpected error reading scale: {e}")
        raise

    finally:
        ser.close()


def get_stored_readings() -> dict:
    '''
    checks for expected scale data retention file. Creates a new one if not exists or corrupted
    '''
    if PERSISTENT_DATA_FILE.exists():
        try:
            with PERSISTENT_DATA_FILE.open("r") as f:
                weight_state = json.load(f)
                
            logger.info(f"Successfully read saved weight statistics from local file: {PERSISTENT_DATA_FILE}")
            return weight_state
        
        except json.JSONDecodeError:
            logger.error("State file corrupted. Using new default state.")

    logger.info(f"Returning default/new weight statistic data")
    return {
        "ewma": None,
        "last_reading": None,
        "order_cooldown": 0
    }
        

def save_stored_readings(state: dict) -> None:
    '''
    saves weight tracking data to expected location.
    '''
    with PERSISTENT_DATA_FILE.open('w') as f:
        json.dump(state, f, indent=4)
        logger.debug(f"Saved weight statistic: {state} to {PERSISTENT_DATA_FILE}")
        
