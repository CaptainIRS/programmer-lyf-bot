'''
Contains the functions to fetch data from devrant API
'''

import logging
import requests


def fetch_rants_json(period: str, limit: int):
    '''
    Fetches required number of rants from given period of time
    :return dict()
    '''
    response = requests.get(
        f'https://devrant.com/api/devrant/rants?app=3&range={period}&sort=top&limit={limit}'
    )
    if response.status_code == 200:
        json_data = response.json()
        if json_data['success']:
            logging.info('devRants fetched successfully')
            return json_data['rants']
        logging.critical('devRant request unsuccessful')
        return None
    logging.critical('devRant request failed with status code: %d', response.status_code)
    return None
