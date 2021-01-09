'''
Contains the APIs for getting rants from devrant
'''

from .fetch import fetch_rants_json


def get_rants(frequency: str, limit: int):
    '''
    Gets rants for given frequency
    '''
    period = ''
    if frequency == 'daily':
        period = 'day'
    elif frequency == 'weekly':
        period = 'week'
    rants = fetch_rants_json(period, limit)
    return rants
