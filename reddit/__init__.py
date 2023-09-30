'''
Contains reddit related functions
'''

import os

import dotenv
from praw import Reddit

from util.load_config import load_config

from .fetch import fetch_reddit_posts


def get_reddit_client():
    '''
    Get reddit client
    '''
    dotenv.load_dotenv(override=True)

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    user_agent = os.getenv('USER_AGENT')

    return Reddit(client_id=client_id,
                  client_secret=client_secret,
                  username=username,
                  password=password,
                  user_agent=user_agent)


def get_reddit_posts(frequency: str, limit: int):
    '''
    Get top reddit posts
    '''

    reddit = get_reddit_client()

    subreddit_json = load_config('reddit.json')['subreddits']
    subreddits = [s for s in subreddit_json if s["frequency"] == frequency]

    posts = fetch_reddit_posts(reddit, subreddits, limit)
    return posts
