from datetime import datetime
from praw import Reddit
from dotenv import load_dotenv
import json
import os

load_dotenv()


def create_post_list(selected_posts):

    posts = []
    image_formats = ['jpg', 'jpeg', 'png', 'gif']

    for post in selected_posts:

        data = {}
        data['title'] = post.title
        data['selftext'] = post.selftext
        data['posted'] = datetime.utcfromtimestamp(post.created_utc).strftime('%a, %d %b %Y %X UTC')
        data['upvotes'] = post.ups
        data['downvotes'] = post.downs
        data['comments'] = post.num_comments
        data['is_video'] = post.is_video
        data['over_18'] = post.over_18
        data['url'] = 'https://www.reddit.com' + post.permalink
        data['media'] = {}

        if post.is_self:  # if post is text-only
            data['media'] = {'url': '', 'medium': 'text'}

        elif post.is_video:
            data['media']['url'] = post.secure_media['reddit_video']['fallback_url']
            data['media']['medium'] = 'video'

        elif post.url.split('.')[-1] in image_formats:
            data['media'] = {'url': post.url, 'medium': 'image'}

        posts.append(data)

    return posts


def fetch_top_posts(subreddit, unwanted_flairs, frequency, limit):

    posts = subreddit.top(time_filter=frequency)
    selected_posts = []

    selected = 0

    for post in posts:
        if selected >= limit:
            break
        if not post.stickied:
            if post.link_flair_text not in unwanted_flairs:
                selected_posts.append(post)
                selected += 1

    return create_post_list(selected_posts)


def do_the_magic(reddit, subreddits, limit):

    frequency_map = {
        'hourly': 'hour',
        'daily': 'day',
        'weekly': 'week',
        'monthly': 'month',
        'yearly': 'year',
        'all': 'all'
    }

    result = {'subreddits': []}

    for obj in subreddits:

        subreddit = reddit.subreddit(obj['subreddit'])
        flairs = obj['unwanted_flairs']
        frequency = frequency_map[obj['frequency']]

        data = {}
        data['subreddit'] = obj['subreddit']
        data['category'] = obj['category']
        data['frequency'] = obj['frequency']
        data['posts'] = fetch_top_posts(subreddit, flairs, frequency, limit)
        data['subreddit_url'] = 'https://www.reddit.com' + subreddit.url
        data['subreddit_icon'] = subreddit.icon_img

        result['subreddits'].append(data)

    return result


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
user_agent = os.getenv('USER_AGENT')

reddit = Reddit(client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=user_agent)

pwd = os.path.dirname(os.path.realpath(__file__))

with open(f'{pwd}/../config/reddit.json') as infile:
    subreddits = json.load(infile)['subreddits']

max_posts_to_fetch = 5
result = do_the_magic(reddit, subreddits, max_posts_to_fetch)
