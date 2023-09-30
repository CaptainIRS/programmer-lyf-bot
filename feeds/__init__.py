'''
APIs for getting feeds
'''

from .fetch import submit_feed_updates


def submit_updates(queue, blog, data_file, limit, frequency):
    '''
    Submit feed updates to queue
    '''
    submit_feed_updates(queue, blog, data_file, limit, frequency)
