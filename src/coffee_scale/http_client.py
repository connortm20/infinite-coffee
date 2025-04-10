'''
http wrapper to handle api requests differences when running on python vs micropython
'''

try:
    import urequests as requests
except ImportError:
    import requests

def get(url, data, headers=None):
    res = requests.get(url, headers=headers)
    return res

def post(url, data, headers=None):
    res = requests.post(url, data=data, headers=headers)
    return res