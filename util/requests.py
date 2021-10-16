'''
APIs to fetch urls from server
'''


import logging
import warnings

import requests

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def fetch_from_server(url: str):
    '''
    Fetch from server and log success/error
    '''
    try:
        response = requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
            },
            timeout=15,
            verify=False
        )
        if response.status_code == 200:
            return response.content.decode('utf-8', 'ignore')
        logging.error(
            'Request to %s failed - %d: %s', url, response.status_code, response.reason
        )
        return None
    except Exception as exception:  # pylint: disable=broad-except
        logging.error('Cannot connect to %s - %s', url, str(exception)[:30])
        return None
