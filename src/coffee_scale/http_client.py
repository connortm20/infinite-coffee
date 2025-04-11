'''
http wrapper to handle api requests differences when running on python vs micropython
'''

import os
import logging
import json

logger = logging.getLogger(__name__)


try:
    import urequests as requests
except ImportError:
    import requests

def get(url, headers=None):
    res = requests.get(url, headers=headers)
    return res

def post(url: str, data=None, headers: dict=None):
    res = requests.post(url, data=data, headers=headers,)
    return res
