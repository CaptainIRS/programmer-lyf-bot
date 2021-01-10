'''
APIs for fetching hackernews posts
'''
import concurrent.futures as futures
import json

from util.requests import fetch_from_server


def _fetch_hackernews_story(story_id):
    story_json = json.loads(
        fetch_from_server(
            f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
        )
    )
    story = {
        'title': story_json["title"],
        'description': f'{story_json["score"]} points',
        'url': story_json["url"] or 'https://news.ycombinator.com/',
        'comments_link': f'[{story_json["descendants"]}\
             comments](https://news.ycombinator.com/item?id={story_id})',
        'author_name': story_json["by"] or '*Not Available*'
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

    top_stories = top_stories[:limit]

    processes = []
    executor = futures.ThreadPoolExecutor(max_workers=30)
    for story_id in top_stories:
        processes.append(executor.submit(_fetch_hackernews_story, story_id))

    posts = []
    for process in futures.as_completed(processes):
        if process.result():
            posts.append(process.result())

    return posts
