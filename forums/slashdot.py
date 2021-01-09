'''
APIs for fetching slashdot posts
'''

from util.feed_utils import transform_feed
from util.requests import fetch_from_server


def fetch_slashdot_posts(limit: int):
    '''
    Fetch slashdot data and transform
    '''
    feed_url = 'http://rss.slashdot.org/Slashdot/slashdotDevelopers'
    details = ('Slashdot', 'https://slashdot.org/', feed_url)
    feed_data = fetch_from_server(feed_url)

    posts = transform_feed(feed_data, details, limit, None)
    return posts
