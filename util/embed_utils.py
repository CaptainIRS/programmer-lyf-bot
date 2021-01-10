'''
Utils for converting from other data formats to discord embeds
'''
import logging

from discord import Colour, embeds

from util.load_config import load_config


class ValidEmbed():
    '''
    Set valid parameters to Discord Embed
    '''

    def __init__(self, **kwargs):
        title = self._truncate(kwargs.get('title', ''), 250)
        description = self._truncate(kwargs.get('description', ''), 2000)
        url = self._validate_url(kwargs.get('url', ''))
        colour = kwargs.get('colour', Colour.purple())
        self.embed = embeds.Embed(
            title=title,
            description=description,
            url=url,
            colour=colour
        )

    def set_author(self, **kwargs):
        '''Set valid author parameters'''
        name = self._truncate(kwargs.get('name', ''), 250)
        url = self._validate_url(kwargs.get('url', ''))
        icon_url = self._validate_url(kwargs.get('icon_url', ''))
        self.embed.set_author(
            name=name,
            url=url,
            icon_url=icon_url
        )

    def set_footer(self, **kwargs):
        '''Set valid footer parameters'''
        text = self._truncate(kwargs.get('text', '-'), 2000)
        if text == '':
            text = '-'
        icon_url = self._validate_url(kwargs.get('icon_url', ''))
        self.embed.set_footer(
            text=text,
            icon_url=icon_url
        )

    def add_field(self, **kwargs):
        '''Set valid field parameters'''
        name = self._truncate(kwargs.get('name', ''), 250)
        if name == '':
            name = '-----'
        value = self._truncate(kwargs.get('value', ''), 1000)
        if value == '':
            value = '*Description not available*'
        self.embed.add_field(
            name=name,
            value=value,
            inline=False
        )

    def set_image(self, **kwargs):
        '''Set valid image parameters'''
        url = self._validate_url(kwargs.get('url', ''))
        self.embed.set_image(
            url=url
        )

    def valid_embed(self):
        '''Return valid discord embed'''
        return self.embed

    @staticmethod
    def _validate_url(url):
        if url == '':
            return url
        if 'http' not in url:
            logging.warning('%s is not a valid URL', url)
            return ''
        return url

    @staticmethod
    def _truncate(string, limit):
        if len(string) > limit:
            string = f'{string[:limit]}...'
        return string


def create_blog_embed(post):
    '''
    Create blog post embed from JSON
    '''
    embed = ValidEmbed(
        title=post["title"],
        description='',
        url=post["url"],
        colour=Colour.blue()
    )

    if 'image' in post:
        embed.set_image(url=post["image"][0]["url"])

    embed.set_author(
        name=post['publisher'],
        url=post['publisher_url'],
        icon_url=post['publisher_image']
    )

    embed.set_footer(
        text=post["author_name"] or post['publisher'],
        icon_url=(post["author_icon"][0]["url"] if 'author_icon' in post else ''),
    )

    embed.add_field(
        name='-----',
        value=post["description"]
    )

    return embed.valid_embed()


def create_devrant_embed(rant):
    '''
    Create devrant embed from JSON
    '''
    embed = ValidEmbed(
        name='',
        description=rant['text'],
        colour=0xf99a66,
    )

    embed.set_author(
        name='devRant',
        url='https://devrant.com',
        icon_url='https://devrant.com/static/devrant/img/favicon32.png'
    )

    embed.set_footer(
        text=f'By {rant["user_username"]}',
        icon_url=f'https://avatars.devrant.com/{rant["user_avatar"]["i"]}'
    )

    if 'attached_image' in rant and 'url' in rant['attached_image']:
        embed.set_image(url=rant["attached_image"]["url"])

    return embed.valid_embed()


def create_reddit_embed(subreddit, post):
    '''
    Create reddit post embed from subreddit JSON
    '''
    selftext = post["selftext"]

    embed = ValidEmbed(
        title=post["title"],
        description=selftext or "\u200b",
        url=post["url"],
        colour=Colour.red()
    )

    if 'media' in post and 'url' in post['media']:
        embed.set_image(url=post["media"]["url"])

    embed.set_author(
        name=f'r/{subreddit["subreddit"]}',
        url=subreddit["subreddit_url"],
        icon_url=subreddit["subreddit_icon"]
    )

    return embed.valid_embed()


def create_forum_embed(forum, post):
    '''
    Create forum embed from JSON
    '''
    config = load_config('forums.json')[forum]
    embed = ValidEmbed(
        title=post["title"],
        description=post["description"],
        url=post["url"],
        colour=config['color']
    )

    if 'image' in post:
        embed.set_image(url=post["image"][0]["url"])

    embed.set_author(
        name=config['publisher'],
        url=config['publisher_url'],
        icon_url=config['icon_url']
    )

    if 'comments_link' in post:
        embed.add_field(
            name='-----',
            value=post['comments_link']
        )

    embed.set_footer(
        text=post["author_name"] or config['publisher'],
        icon_url=(post["author_icon"][0]["url"] if 'author_icon' in post else ''),
    )

    return embed.valid_embed()
