from praw import Reddit
from datetime import datetime
import json


def create_post_list(selected_posts):

    posts = []

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
        data['media'] = {'url': post.url, 'medium': 'video' if post.is_video else 'image'}

        posts.append(data)

    return posts


def fetch_top_posts(subreddit, unwanted_flairs, frequency, limit):

    posts = subreddit.top(time_filter=frequency)
    selected_posts = []

    selected = 0
    total = 0

    for post in posts:
        if selected >= limit or total >= 100:
            break
        if not post.stickied:
            if post.link_flair_text not in unwanted_flairs:
                selected_posts.append(post)
                selected += 1
        total += 1

    return create_post_list(selected_posts)


def do_the_magic(reddit, subreddits):

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
        data['posts'] = fetch_top_posts(subreddit, unwanted_flairs, frequency, 5)
        data['subreddit_url'] = 'https://www.reddit.com' + subreddit.url
        data['subreddit_icon'] = subreddit.icon_img

        result['subreddits'].append(data)

    return result


def main():

    client_id = '8-vcJfTwkfFq4Q'
    client_secret = 'JMaRi5KcdHZ-LyLn6gvDd71U-tg9hQ'

    reddit = Reddit(client_id=client_id,
                    client_secret=client_secret,
                    username='anuraggoyalawr',
                    password='CR237ZAG20',
                    user_agent='mybot-v1')

    with open('./config.json') as infile:
        subreddits = json.load(infile)['subreddits']

    result = do_the_magic(reddit, subreddits)

    with open(f'./result.json', 'w') as outfile:
        outfile.write(json.dumps(result, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
