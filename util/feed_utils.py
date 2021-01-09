'''
Utilities for parsing feeds
'''

import collections
import logging
from datetime import datetime, timedelta
from time import mktime

import feedparser
from util.markdown import markdownify


def _feed_to_post(feed, feed_entry, details):
    publisher, publisher_url, _ = details

    data = collections.defaultdict(str)

    data['publisher'] = feed.title if hasattr(feed, 'title') else publisher
    data['publisher_url'] = feed.link if hasattr(feed, 'link') else publisher_url
    if hasattr(feed, 'image'):
        data['publisher_image'] = feed.image.link

    data['title'] = feed_entry.title
    description = markdownify(feed_entry.summary)
    if len(description) > 1000:
        description = f'{description[:1000]}...'
    data['description'] = description
    data['url'] = feed_entry.link

    if hasattr(feed_entry, 'media_content'):
        data['image'] = feed_entry.media_content
    elif hasattr(feed, 'image'):
        data['image'] = feed.image.link

    if hasattr(feed_entry, 'author_detail'):
        if hasattr(feed_entry.author_detail, 'name'):
            data['author_name'] = feed_entry.author_detail.name
        if hasattr(feed_entry.author_detail, 'href'):
            data['author_url'] = feed_entry.author_detail.href

    if hasattr(feed_entry, 'media_thumbnail'):
        data['author_icon'] = feed_entry.media_thumbnail

    return data


def transform_feed(feed_data, details, limit, time_delta=timedelta(1)):
    '''
    Function to transform feed to required json format
    '''

    _, publisher_url, feed_data = details

    if not feed_data:
        return []

    feed = feedparser.parse(feed_data)
    feed_entries = feed.entries[:limit]
    if time_delta:
        feed_entries = [
            entry for entry in feed_entries
            if hasattr(entry, 'published_parsed')
            and datetime.fromtimestamp(mktime(entry.published_parsed))
            > datetime.utcnow() - time_delta
        ]
    if feed_entries:
        logging.info('Fetching %d articles from %s', len(feed_entries), publisher_url)
    else:
        logging.info('No article for %s', publisher_url)

    posts = []

    for feed_entry in feed_entries:
        post = _feed_to_post(feed, feed_entry, details)
        posts.append(post)

    return posts
