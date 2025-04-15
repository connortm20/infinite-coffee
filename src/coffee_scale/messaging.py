import logging
import json
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from http_client import post
from config import config

TEXTBELT_KEY = config['TEXTBELT_KEY']
TO_PHONE_NUMBER = config['TO_PHONE_NUMBER']
WEBHOOK_URL = config['WEBHOOK_URL']
WEBHOOK_PORT = config['WEBHOOK_PORT']
WEBHOOK_TIMEOUT = config['WEBHOOK_TIMEOUT']

logger = logging.getLogger(__name__)

incoming_response = None

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global incoming_response

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
             parsed_body = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON from webhook body: %s", e)

        incoming_response = {
            'headers': dict(self.headers),
            'body': parsed_body,
            'client_address': self.client_address,
            'path': self.path,
            'command': self.command,
        }

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "received"}')

    def log_message(self, format, *args):
        logger.info("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        ))


def run_single_request_listener(port, total_timeout, check_interval=5):
    """
    Starts a temporary HTTP server that waits for a single POST request
    or until the total_timeout period expires.
    - port: Port number on which the server will listen.
    - total_timeout: Total seconds to wait before giving up.
    - check_interval: How long (in seconds) to wait for each loop iteration.
    """
    global incoming_response
    incoming_response = None

    server = HTTPServer(('', port), WebhookHandler)
    server.socket.settimeout(check_interval)
    
    start_time = time.time()
    logger.info(f"Starting listener on port {port}; waiting for up to {total_timeout} seconds...")

    while time.time() - start_time < total_timeout:
        try:
            server.handle_request()
        except socket.timeout:
            pass

        if incoming_response is not None:
            logger.info(f"Post request received")
            break

    return incoming_response



def send_message_and_wait() -> bool:
    url = 'https://textbelt.com/text'
    
    data = {
        'phone': TO_PHONE_NUMBER,
        'message': 'Your coffee reserves were detected to be low. Do you wish to place a new order of your configured coffee preference? Reply "Y" or "N"',
        'key': TEXTBELT_KEY,
        'replyWebhookUrl': f'{WEBHOOK_URL}:{WEBHOOK_PORT}',
    }

    logger.info('Sending configured alert message')
    res = post(url, data)
    logger.debug(f'Message send response: {res.text}')

    if res.status_code != 200:
        logging.error(f'sms message did not receive success code. res: {res.text}')
        raise

    sent_textId = res.json()['textId']

    webhook_res = run_single_request_listener(int(WEBHOOK_PORT), int(WEBHOOK_TIMEOUT))

    if not webhook_res:
        logger.info(f'No webhook POST received. Timeout set at: {WEBHOOK_TIMEOUT} seconds')
        return False
    
    logger.debug(f'Webhook received: {webhook_res}')

    #light validation for webhook post
    rec_textId = str(webhook_res['body']['textId'])
    if rec_textId != sent_textId:
        logger.error(f'MISMATCH TEXTID BETWEEN SENT AND RECEIVED MESSAGES. post received : {webhook_res.text}')
        raise Exception('invalid or corrupt webhook data recieved')

    rec_from_number = str(webhook_res['body']['fromNumber'])
    if rec_from_number != TO_PHONE_NUMBER:
        logger.error(f'MISMATCH FROMNUMBER BETWEEN SENT AND RECEIVED MESSAGES. post received : {webhook_res.text}')
        raise Exception('invalid or corrupt webhook data recieved')
   
   
    message_text = str(webhook_res['body']['text'])
    if message_text.strip().lower() == 'y':
        return True

    return False

