'''
APIs for getting feeds
'''

from .fetch import fetch_feed


def get_feed(data_file, limit, frequency):
    '''
    Get feed
    '''
    return fetch_feed(data_file, limit, frequency)
