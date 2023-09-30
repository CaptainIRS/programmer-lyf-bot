'''
Utilities for parsing feeds
'''

import collections
import logging
import re
from calendar import timegm
from datetime import datetime, timedelta

import feedparser

from util.markdown import markdownify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/tmp/debug.log"),
        logging.StreamHandler()
    ]
)


def _get_image(feed_entry):
    if 'featuredImage' in feed_entry:
        return feed_entry.featuredImage

    if 'media_content' in feed_entry \
            and len(feed_entry.media_content) > 0 \
            and 'url' in feed_entry.media_content[0]:
        return feed_entry.media_content[0]['url']

    if 'media_thumbnail' in feed_entry:
        if 'url' in feed_entry.media_thumbnail:
            return feed_entry.media_thumbnail['url']
        if 'url' in feed_entry.media_thumbnail[0]:
            return feed_entry.media_thumbnail[0]['url']

    if 'content' in feed_entry \
            and len(feed_entry.content[0]) > 0 \
            and 'value' in feed_entry.content[0] \
            and re.search(
                r'(?P<url>http.?://[^\s]+(png|jpeg|jpg))',
                feed_entry.content[0].value
            ):
        return re.search(
            r'(?P<url>http.?://[^\s]+(png|jpeg|jpg))',
            feed_entry.content[0].value
        ).group("url") or ''

    return ''


def _feed_to_post(feed, feed_entry, details):
    publisher, publisher_url, _ = details

    data = collections.defaultdict(str)

    data['publisher'] = publisher
    data['publisher_url'] = publisher_url
    if 'image' in feed and 'href' in feed.image:
        data['publisher_image'] = feed.image.href

    if 'title' in feed_entry:
        data['title'] = feed_entry.title

    if 'summary' in feed_entry:
        data['description'] = markdownify(feed_entry.summary)

    if 'link' in feed_entry:
        data['url'] = feed_entry.link

    data['image'] = _get_image(feed_entry)

    if 'author_detail' in feed_entry:
        if 'name' in feed_entry.author_detail:
            data['author_name'] = feed_entry.author_detail.name
        if 'href' in feed_entry.author_detail:
            data['author_url'] = feed_entry.author_detail.href

    if 'media_thumbnail' in feed_entry:
        data['author_icon'] = feed_entry.media_thumbnail

    return data


def _check_if_within_time(published_time, time_delta):
    try:
        published_timestamp = datetime.utcfromtimestamp(timegm(published_time))
        current_timestamp = datetime.utcnow()
        return current_timestamp - time_delta < published_timestamp <= current_timestamp
    except Exception as exception:  # pylint: disable=broad-except
        logging.error(exception)
        return False


def transform_feed(feed_data, details, limit, time_delta=timedelta(1)):  # pylint: disable=too-many-locals
    '''
    Function to transform feed to required json format
    '''

    _, publisher_url, feed_url = details

    if not feed_data:
        return []
    try:
        feed_object = feedparser.parse(feed_data)
    except Exception as exception:  # pylint: disable=broad-except
        logging.error(
            'Error when parsing feed from %s.\nFeed data: %s\nException: %s',
            feed_url,
            feed_data,
            exception
        )
        return []
    feed_entries = feed_object.entries[:limit]
    if time_delta:
        feed_entries = [
            entry for entry in feed_entries
            if (hasattr(entry, 'published_parsed') and entry.published_parsed
                and _check_if_within_time(entry.published_parsed, time_delta)) or
            (not hasattr(entry, 'published_parsed') and hasattr(entry, 'updated_parsed')
                and entry.updated_parsed
                and _check_if_within_time(entry.updated_parsed, time_delta))
        ]
    if feed_entries:
        logging.info('Fetching %d articles from %s', len(feed_entries), publisher_url)
    else:
        if feed_object.entries and hasattr(feed_object.entries[0], 'published_parsed'):
            try:
                last_published = datetime.utcfromtimestamp(timegm(feed_object.entries[0].published_parsed))
                delta = datetime.utcnow() - last_published
                stale = ''
                if delta.days > 365:
                    stale = 'Stale publication. '
                logging.info('%sNo article for %s, last published %s days ago', stale, publisher_url, delta.days)
            except Exception:  # pylint: disable=broad-except
                logging.error('Timestamps invalid in %s', feed_url)
        else:
            logging.error('Invalid feed entry for %s at %s. Please check.', publisher_url, feed_url)

    posts = []

    for feed_entry in feed_entries:
        if 'published_parsed' not in feed_entry:
            feed_entry.published_parsed = feed_entry.updated_parsed
        post = _feed_to_post(feed_object.feed, feed_entry, details)
        posts.append(post)

    return posts
