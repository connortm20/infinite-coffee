import logging
import base64

from http_client import get, post
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM_PHONE_NUMBER, TO_PHONE_NUMBER

logger = logging.getLogger(__name__)


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

    return res


