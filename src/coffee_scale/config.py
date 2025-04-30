import os
from dotenv import load_dotenv
from typing import Callable, Any, Dict
import logging

logger = logging.getLogger(__name__)


def load_env_config(required_vars: dict[str, Callable[[str], Any]]) -> Dict[str, Any]:
    '''
    Loads all configured env variables into the config dictionary as their mapped types
    '''
    load_dotenv()

    config = {}
    missing_vars = []
    failed_conversions = []
    
    for var,type in required_vars.items():
        value = os.getenv(var)

        if value is None:
            missing_vars.append(var)
            continue

        try:
            config[var] = type(value)
        except Exception as e:
            failed_conversions.append(f'{var}:{value}:{type}')

    if missing_vars:
        logger.error(f'mising env vars detected : {missing_vars}')

    if failed_conversions:
        logger.error(f'failed env type conversion : {failed_conversions}')

    return config


REQUIRED_VARS = {
    'TEXTBELT_KEY': str,
    'TO_PHONE_NUMBER': str,
    'WEBHOOK_URL': str,
    'WEBHOOK_PORT': str,
    'WEBHOOK_TIMEOUT': str,
    'TERMINAL_SHOP_TOKEN': str,
    'EWMA_ALPHA': float,
    'STANDARD_DELIVERY_TIME': int,
    'DEFAULT_COOLDOWN_LENGTH': int,
    'SCALE_SERIAL_PORT': str,
}

config = load_env_config(REQUIRED_VARS)
