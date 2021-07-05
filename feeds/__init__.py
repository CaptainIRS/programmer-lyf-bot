'''
APIs for getting feeds
'''

from .fetch import *


def get_blog_posts(data_file, limit, frequency):
    return fetch_feed(data_file, limit, frequency, "blog")


def get_podcasts(data_file, limit, frequency):
    return fetch_feed(data_file, limit, frequency, "podcasts")
