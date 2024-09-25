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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
            },
            timeout=25,
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


def fetch_image_to_file(url: str, filename: str):
    '''
    Fetch image from server and save to file
    '''
    try:
        response = requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
            },
            timeout=25,
            verify=False
        )
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
        logging.error(
            'Request to %s failed - %d: %s', url, response.status_code, response.reason
        )
        return False
    except Exception as exception:  # pylint: disable=broad-except
        logging.error('Cannot connect to %s - %s', url, str(exception)[:30])
        return False
