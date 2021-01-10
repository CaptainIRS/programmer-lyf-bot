'''
APIs for getting posts from forums like slashdot and hackernews
'''

from .slashdot import fetch_slashdot_posts
from .hackernews import fetch_hackernews_posts


def get_forum_posts(forum: str, limit: int) -> list:
    '''
    Get slashdot posts
    '''

    if forum == 'slashdot':
        posts = fetch_slashdot_posts(limit)
    elif forum == 'hackernews':
        posts = fetch_hackernews_posts(limit)
    else:
        posts = []

    return posts
