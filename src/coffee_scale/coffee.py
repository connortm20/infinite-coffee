from typing import Optional
from dotenv import load_dotenv


TERMINAL_SHOP_TOKEN: Optional[str] = None

TERMINAL_URL = 'https://api.dev.terminal.shop'

from config import TERMINAL_SHOP_TOKEN
from http_client import get, post


def set_card():

    stripe_token = 'foobar'
    print(TERMINAL_SHOP_TOKEN)
    url = f'{TERMINAL_URL}/card'
    headers = {
         'Authorization': f'Bearer {TERMINAL_SHOP_TOKEN}'
    }
    body = {
        'token': stripe_token
    }

    res = post(url, body, headers)

    print(res.text)


set_card()