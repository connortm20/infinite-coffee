from typing import Optional

TWILIO_ACCOUNT_SID: Optional[str] = None
TWILIO_AUTH_TOKEN: Optional[str] = None
FROM_PHONE_NUMBER: Optional[str] = None
TO_PHONE_NUMBER: Optional[str] = None


import os
import logging
from dotenv import load_dotenv
import base64

from http_client import get, post

logger = logging.getLogger(__name__)

def load_required_vars():
    load_dotenv()
    required_vars = ['TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','FROM_PHONE_NUMBER','TO_PHONE_NUMBER']
    missing_vars = []

    for var in required_vars:
        val = os.getenv(var)
        if val is None:
            missing_vars.append(var)
        else:
            globals()[var] = val

    if missing_vars:
        logger.error(f'Missing env vars detected/failed to load: {missing_vars}')

load_required_vars()



def send_message():
    url = f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json'
    auth = base64.b64encode(f'{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}'.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth}'
    }
    
    data = {
        'From': FROM_PHONE_NUMBER,
        'To': TO_PHONE_NUMBER,
        'Body': 'Your coffee reserves were detected to be low. Do you wish to place a new order of your configured coffee preference? Reply "Y" or "N"'
    }

    logger.info('Sending configured alert message')
    res = post(url, data, headers)


