import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

PERSISTENT_DATA_FILE = Path('weight.json')


def read_scale() -> float:
    reading = 69.69
    logger.info(f"Weight reading of '{reading}' recorded")
    return reading


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
        "last_reading": None
    }
        

def save_stored_readings(state: dict) -> None:
    '''
    saves weight tracking data to expected location.
    '''
    with PERSISTENT_DATA_FILE.open('w') as f:
        json.dump(state, f, indent=4)
        logger.info(f"Saved weight statistic: {state} to {PERSISTENT_DATA_FILE}")
        
