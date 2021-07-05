'''
Contains functions to fetch reddit posts
'''

from datetime import datetime

from markdown import Markdown

from util.markdown import markdownify


def _create_post_list(selected_posts):

    posts = []
    image_formats = ['jpg', 'jpeg', 'png', 'gif']

    markdown = Markdown()

    for post in selected_posts:

        data = {}
        data['title'] = post.title
        data['selftext'] = markdownify(markdown.convert(post.selftext))
        data['posted'] = datetime.utcfromtimestamp(post.created_utc).strftime('%a, %d %b %Y %X UTC')
        data['upvotes'] = post.ups
        data['downvotes'] = post.downs
        data['comments'] = post.num_comments
        data['is_video'] = post.is_video
        data['over_18'] = post.over_18
        data['url'] = 'https://www.reddit.com' + post.permalink
        data['media'] = {}

        if post.is_video:
            data['media']['url'] = post.secure_media['reddit_video']['fallback_url']
            data['media']['medium'] = 'video'

        elif post.url.split('.')[-1].lower() in image_formats:
            data['media'] = {'url': post.url, 'medium': 'image'}

        posts.append(data)

    return posts


def _fetch_top_posts(subreddit, unwanted_flairs, frequency, limit):

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

    return _create_post_list(selected_posts)


def fetch_reddit_posts(reddit, subreddits, limit):
    '''
    Fetches Reddit posts
    '''

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

        unwanted_flairs = obj['unwanted_flairs']
        frequency = frequency_map[obj['frequency']]

        data = {}
        data['subreddit'] = obj['subreddit']
        data['category'] = obj['category']
        data['frequency'] = obj['frequency']
        data['posts'] = _fetch_top_posts(subreddit, unwanted_flairs, frequency, limit)
        data['subreddit_url'] = 'https://www.reddit.com' + subreddit.url
        data['subreddit_icon'] = subreddit.icon_img

        result['subreddits'].append(data)

    return result
