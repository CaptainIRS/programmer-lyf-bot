'''
Utils for converting from other data formats to discord/telegram embeds
'''
import logging
from dataclasses import dataclass

from discord import Colour, embeds

from util.load_config import load_config
from util.markdown import htmlify


class ValidEmbed():
    '''
    Set valid parameters to Discord Embed
    '''

    def __init__(self, **kwargs):
        title = self._truncate(kwargs.get('title', '').strip(), 250)
        description = self._truncate(kwargs.get('description', '').strip(), 2000)
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
        name = self._truncate(kwargs.get('name', '').strip(), 250)
        url = self._validate_url(kwargs.get('url', ''))
        icon_url = self._validate_url(
            kwargs.get(
                'icon_url',
                'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Pan_Blue_Circle.png/30px-Pan_Blue_Circle.png'
            )
        )
        if icon_url == '':
            icon_url = 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Article_Clayton.png'
        icon_url = 'https://images.weserv.nl/?url=' + icon_url + \
            '&output=png&bg=black&w=100&h=100&fit=contain&cbg=black'
        self.embed.set_author(
            name=name,
            url=url,
            icon_url=icon_url
        )

    def set_footer(self, **kwargs):
        '''Set valid footer parameters'''
        text = self._truncate(kwargs.get('text', '-').strip(), 2000)
        if text == '':
            text = '-'
        icon_url = self._validate_url(kwargs.get('icon_url', '')).strip()
        if icon_url == '':
            icon_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/' \
                'Ic_account_circle_48px.svg/200px-Ic_account_circle_48px.svg.png'
        icon_url = f'https://images.weserv.nl/?url={icon_url}&output=png&bg=white&w=100&h=100&fit=contain&cbg=white'
        self.embed.set_footer(
            text=text,
            icon_url=icon_url
        )

    def add_field(self, **kwargs):
        '''Set valid field parameters'''
        name = self._truncate(kwargs.get('name', '').strip(), 250)
        if name == '':
            name = '-----'
        value = self._truncate(kwargs.get('value', '').strip(), 1000)
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
        if url != '':
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
            string = f'{string[:limit]}[...]'
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
        embed.set_image(url=post["image"])

    embed.set_author(
        name=post['publisher'],
        url=post['publisher_url'],
        icon_url=post['publisher_image']
    )

    embed.set_footer(
        text=post["author_name"] or post['publisher'],
        icon_url=(post["author_icon"][0]["url"] if 'author_icon' in post else post['publisher_image']),
    )

    embed.add_field(
        name='-----',
        value=post["description"]
    )

    return embed.valid_embed()


def create_reddit_embed(subreddit, post):
    '''
    Create reddit post embed from subreddit JSON
    '''
    selftext = post["selftext"]

    embed = ValidEmbed(
        title=post["title"],
        description=selftext or "-----",
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

    if 'image' in post and len(post['image']) > 0 and 'url' in post['image'][0]:
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


@dataclass
class TelegramPost:
    '''
    Telegram post
    '''
    message: str
    image_url: str
    show_preview: bool = False


def create_reddit_telegram_post(subreddit, post):
    '''
    Create reddit post embed from subreddit JSON
    '''
    message = f'💬 r/{subreddit["subreddit"]}'
    message += f'\n\n**[{post["title"]}]({post["url"]})**'
    if post["selftext"]:
        if len(post["selftext"]) > 1000:
            post["selftext"] = post["selftext"][:1000] + '...'
        message += f'\n\n{post["selftext"].strip()}'
    message += '\n‎'

    return TelegramPost(
        message=htmlify(message),
        image_url=post["media"]["url"] if 'media' in post and 'url' in post['media'] else ''
    )


def create_forum_telegram_post(forum, post):
    '''
    Create forum embed from JSON
    '''
    config = load_config('forums.json')[forum]

    message = f'💬 {config["publisher"]}'
    message += f'\n\n**[{post["title"]}]({post["url"]})**'
    if post["description"]:
        if len(post["description"]) > 1000:
            post["description"] = post["description"][:1000] + '...'
        message += f'\n\n{post["description"]}'
    if 'comments_link' in post:
        while '  ' in post['comments_link']:
            post['comments_link'] = post['comments_link'].replace('  ', ' ')
        message += f'\n\n{post["comments_link"]}'
    message += '\n‎'

    return TelegramPost(
        message=htmlify(message),
        show_preview=True,
        image_url=post["image"][0]["url"] if 'image' in post and len(
            post['image']) > 0 and 'url' in post['image'][0] else ''
    )


def create_blog_telegram_post(post):
    '''
    Create blog post embed from JSON
    '''
    message = f'📰 {post["publisher"]}'
    message += f'\n\n**[{post["title"]}]({post["url"]})**'
    if post["description"]:
        if len(post["description"]) > 1000:
            post["description"] = post["description"][:1000] + '...'
        message += f'\n\n{post["description"].strip()}'
    message += '\n‎'
    while '\n\n\n' in message:
        message = message.replace('\n\n\n', '\n\n')
    return TelegramPost(
        message=htmlify(message),
        show_preview=not ('image' in post and len(post['image']) > 0),
        image_url=post["image"] if 'image' in post and len(post['image']) > 0 else ''
    )


@dataclass
class RedditPost:
    '''
    Reddit post
    '''
    title: str
    description: str
    url: str


def create_forum_reddit_post(forum, post):
    '''
    Create forum embed from JSON
    '''
    config = load_config('forums.json')[forum]

    title = f'💬 {config["publisher"]} - {post["title"]}'
    description = post["description"]
    url = None
    if description:
        description += f'\n\n[Link to post and comments]({post["url"]})'
    else:
        url = post["url"]

    return RedditPost(
        title=title,
        description=description,
        url=url
    )


def create_blog_reddit_post(post):
    '''
    Create blog post embed from JSON
    '''
    title = f'📰 {post["publisher"]} - {post["title"]}'
    description = post["description"]
    url = None
    if description:
        description += f'\n\n[Link to post]({post["url"]})'
    else:
        url = post["url"]

    return RedditPost(
        title=title,
        description=description,
        url=url
    )


@dataclass
class MatrixPost:
    '''
    Matrix post
    '''
    markdown: str
    image_url: str = None


def create_forum_matrix_post(forum, post):
    '''
    Create forum embed from JSON
    '''
    config = load_config('forums.json')[forum]

    message = f'***\n\n💬 {config["publisher"]}'
    message += f'\n\n**[{post["title"]}]({post["url"]})**'
    if post["description"]:
        if len(post["description"]) > 1000:
            post["description"] = post["description"][:1000] + '...'
        message += f'\n\n{post["description"]}'
    if 'comments_link' in post:
        while '  ' in post['comments_link']:
            post['comments_link'] = post['comments_link'].replace('  ', ' ')
        message += f'\n\n{post["comments_link"]}'
    message += '\n‎'

    return MatrixPost(
        markdown=message
    )


def create_blog_matrix_post(post):
    '''
    Create blog post embed from JSON
    '''
    message = f'***\n\n📰 {post["publisher"]}'
    message += f'\n\n**[{post["title"]}]({post["url"]})**'
    image_url = post["image"] if 'image' in post and len(post['image']) > 0 else ''
    if image_url:
        message += f'\n\n![]({image_url})'
    if post["description"]:
        if len(post["description"]) > 1000:
            post["description"] = post["description"][:1000] + '...'
        message += f'\n\n{post["description"].strip()}'
    message += '\n‎'
    while '\n\n\n' in message:
        message = message.replace('\n\n\n', '\n\n')

    return MatrixPost(
        markdown=message,
        image_url=image_url
    )


def create_reddit_matrix_post(subreddit, post):
    '''
    Create reddit post embed from subreddit JSON
    '''
    message = f'***\n\n💬 r/{subreddit["subreddit"]}'
    message += f'\n\n**[{post["title"]}]({post["url"]})**'
    image_url = post["media"]["url"] if 'media' in post and 'url' in post['media'] else ''
    if image_url:
        message += f'\n\n![]({image_url})'
    if post["selftext"]:
        if len(post["selftext"]) > 1000:
            post["selftext"] = post["selftext"][:1000] + '...'
        message += f'\n\n{post["selftext"].strip()}'
    message += '\n‎'

    return MatrixPost(
        markdown=message,
        image_url=image_url
    )
