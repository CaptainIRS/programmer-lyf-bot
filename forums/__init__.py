'''
APIs for getting posts from forums like slashdot and hackernews
'''

from .hackernews import fetch_hackernews_posts
from .slashdot import fetch_slashdot_posts


def get_forum_posts(forum: str, limit: int) -> list:
    '''
    Get forum posts
    '''

    if forum == 'slashdot':
        posts = fetch_slashdot_posts(limit)
    elif forum == 'hackernews':
        posts = fetch_hackernews_posts(limit)
    else:
        posts = []

    return posts
