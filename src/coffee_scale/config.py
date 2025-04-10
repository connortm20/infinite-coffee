import os
from dotenv import load_dotenv
from typing import Optional
import logging

logger = logging.getLogger(__name__)


REQUIRED_VARS = [
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'FROM_PHONE_NUMBER',
    'TO_PHONE_NUMBER',
    'TERMINAL_SHOP_TOKEN',
]
TWILIO_ACCOUNT_SID: Optional[str] = None
TWILIO_AUTH_TOKEN: Optional[str] = None
FROM_PHONE_NUMBER: Optional[str] = None
TO_PHONE_NUMBER: Optional[str] = None
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