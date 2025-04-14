import os
from dotenv import load_dotenv
from typing import Optional
import logging

logger = logging.getLogger(__name__)


REQUIRED_VARS = [
    'TEXTBELT_KEY',
    'TO_PHONE_NUMBER',
    'WEBHOOK_URL',
    'WEBHOOK_PORT',
    'WEBHOOK_TIMEOUT',
    'TERMINAL_SHOP_TOKEN'
]
TEXTBELT_KEY: Optional[str] = None
TO_PHONE_NUMBER: Optional[str] = None
WEBHOOK_URL: Optional[str] = None
WEBHOOK_PORT: Optional[str] = None
WEBHOOK_TIMEOUT: Optional[str] = None
TERMINAL_SHOP_TOKEN: Optional[str] = None


def load_required_vars(required_vars: list[str]):
    missing_vars = []

    for var in required_vars:
        val = os.getenv(var)
        if val is None:
            missing_vars.append(var)
        else:
            globals()[var] = val

    if missing_vars:
        logger.error(f'Missing env vars detected/failed to load: {missing_vars}')


load_dotenv()
load_required_vars(REQUIRED_VARS)