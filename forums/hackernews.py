'''
APIs for fetching hackernews posts
'''
import json
from concurrent import futures

from util.requests import fetch_from_server


def _fetch_hackernews_story(story_id):
    story_json = json.loads(
        fetch_from_server(
            f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
        )
    )
    story = {
        'title': story_json["title"],
        'description': f'{story_json["score"] if "score" in story_json else 0} points',
        'url': story_json["url"] if 'url' in story_json else 'https://news.ycombinator.com/',
        'comments_link': f'[{story_json["descendants"] if "descendants" in story_json else 0}\
             comments](https://news.ycombinator.com/item?id={story_id})',
        'author_name': story_json["by"] if 'by' in story_json else '*Not Available*',
        'points': story_json["score"] if 'score' in story_json else 0,
    }
    return story


def fetch_hackernews_posts(limit: int):
    '''
    Fetch hackernews data
    '''
    top_stories = json.loads(
        fetch_from_server(
            'https://hacker-news.firebaseio.com/v0/topstories.json'
        )
    )

    processes = []
    executor = futures.ThreadPoolExecutor(max_workers=10)
    for story_id in top_stories:
        processes.append(executor.submit(_fetch_hackernews_story, story_id))

    posts = []
    for process in futures.as_completed(processes):
        if process.result():
            posts.append(process.result())

    posts.sort(key=lambda p: p['points'], reverse=True)
    return posts[:limit]
