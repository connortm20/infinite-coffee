import json
import logging
logger = logging.getLogger(__name__)

from http_client import get, post, put
from config import TERMINAL_SHOP_TOKEN

TERMINAL_URL = 'https://api.dev.terminal.shop'
STANDARD_HEADERS = {
        'Authorization': f'Bearer {TERMINAL_SHOP_TOKEN}',
        'Content-Type': 'application/json'
    }

def get_address_id():
    url = f'{TERMINAL_URL}/address'
    res = get(url, STANDARD_HEADERS)
    logger.debug(f'get_address_id response: {res.text}')
    return res.json()['data'][0]['id']

def get_card_id():
    url = f'{TERMINAL_URL}/card'
    res = get(url, STANDARD_HEADERS)
    logger.debug(f'get_card_id response: {res.text}')
    return res.json()['data'][0]['id']

def exec_default_order(card_id: str, address_id: str):
    url = f'{TERMINAL_URL}/order'
    data = json.dumps({
        'cardID': card_id,
        'addressID': address_id,
        'variants' : {
            'var_01JNH7GTF9FBA62Y0RT0WMK3BT': 1, #flow 
            'var_01J1JFE53306NT180RC4HGPWH8': 1  #object object
        }
    })

    res = post(url, data, STANDARD_HEADERS)
    logger.debug(f'exec_default_order response: {res.text}')
    return res.json()['data']



