'''
Utils for converting from other data formats to discord embeds
'''

from discord import embeds, Colour

from util.load_config import load_config


def create_blog_embed(post):
    '''
    Create blog post embed from JSON
    '''
    embed = embeds.Embed(
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
        text=post["author_name"],
        icon_url=(post["author_icon"][0]["url"] if 'author_icon' in post else ''),
    )

    embed.add_field(
        name='-----',
        value=post["description"]
    )

    return embed


def create_devrant_embed(rant):
    '''
    Create devrant embed from JSON
    '''
    embed_object = embeds.Embed(
        name='',
        description=rant['text'],
        color=0xf99a66,
    ).set_author(
        name='devRant',
        url='https://devrant.com',
        icon_url='https://devrant.com/static/devrant/img/favicon32.png'
    ).set_footer(
        text=f'By {rant["user_username"]}',
        icon_url=f'https://avatars.devrant.com/{rant["user_avatar"]["i"]}'
    )
    if rant['attached_image'] != '':
        embed_object.add_field(
            name='',
            value=f'![{rant["attached_image"]["url"]}]({rant["attached_image"]["url"]})',
            inline=False
        )
    return embed_object


def create_reddit_embed(subreddit, post):
    '''
    Create reddit post embed from subreddit JSON
    '''
    selftext = post["selftext"]
    if selftext == "":
        selftext = "\u200b"

    embed = embeds.Embed(
        title=post["title"],
        description=selftext,
        url=post["url"],
        colour=Colour.red()
    )

    if post["media"]["url"] != "":
        embed.set_image(url=post["media"]["url"])

    embed.set_author(
        name=f'r/{subreddit["subreddit"]}',
        url=subreddit["subreddit_url"],
        icon_url=subreddit["subreddit_icon"]
    )

    return embed


def create_forum_embed(forum, post):
    '''
    Create forum embed from JSON
    '''
    config = load_config('forums.json')[forum]
    embed = embeds.Embed(
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

    embed.set_footer(
        text=post["author_name"],
        icon_url=(post["author_icon"][0]["url"] if 'author_icon' in post else ''),
    )

    return embed
