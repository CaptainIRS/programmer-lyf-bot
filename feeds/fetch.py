'''
Blog fetch
'''

import concurrent.futures as futures
import logging
import time
from datetime import timedelta

import opml

from util.feed_utils import transform_feed
from util.requests import fetch_from_server

logging.basicConfig(level=logging.INFO)


def _process_feed(details, limit, frequency):

    _, __, feed_url = details
    feed_data = fetch_from_server(feed_url)
    if frequency == 'daily':
        day_delta = timedelta(1)
    elif frequency == 'weekly':
        day_delta = timedelta(7)
    else:
        day_delta = None

    return transform_feed(feed_data, details, limit, day_delta)


def fetch_feed(data_file, limit, frequency):
    '''
    Fetch feeds from collection
    '''

    start = time.time()

    feed_details = []

    outlines = opml.parse(data_file)[0]
    for outline in outlines:
        feed_details.append((outline.text, outline.htmlUrl, outline.xmlUrl))

    processes = []
    executor = futures.ThreadPoolExecutor(max_workers=10)
    for feed_detail in feed_details:
        print(feed_detail)
        processes.append(
            executor.submit(_process_feed, feed_detail, limit, frequency)
        )

    posts = []
    for process in futures.as_completed(processes):
        if process.result():
            posts.extend(process.result())

    logging.info(
        'Feeds fetched from %s fetched in %ss', data_file, (time.time() - start)
    )

    return posts
