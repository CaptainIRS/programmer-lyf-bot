'''
Blog fetch
'''

import concurrent.futures as futures
import logging
import time

import opml

from util.feed_utils import transform_feed
from util.requests import fetch_from_server


logging.basicConfig(level=logging.INFO)


def _process_feed(details):

    _, __, feed_url = details
    feed_data = fetch_from_server(feed_url)

    return transform_feed(feed_data, details, 3)


async def get_blog_posts():
    '''
    Fetch blog posts from collection
    '''

    start = time.time()

    feed_details = []

    outlines = opml.parse('data/engineering_blogs.opml')[0]
    for outline in outlines:
        feed_details.append((outline.text, outline.htmlUrl, outline.xmlUrl))

    processes = []
    executor = futures.ThreadPoolExecutor(max_workers=200)
    for feed_detail in feed_details:
        processes.append(executor.submit(_process_feed, feed_detail))

    for process in futures.as_completed(processes):
        if process.result():
            yield process.result()

    logging.info('Blog posts fetched in %ss', (time.time() - start))
