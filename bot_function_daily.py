'''
Bot functions
'''

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor

import aioschedule as schedule
from discord.ext import commands
from dotenv import load_dotenv

import feeds
import devrant
import forums
import reddit
from util.embed_utils import (create_blog_embed, create_devrant_embed,
                              create_forum_embed, create_reddit_embed)
from util.load_config import load_config

logging.basicConfig(level=logging.INFO)

load_dotenv(override=True)

TOKEN = os.getenv('DISCORD_TOKEN')

reddit_channels = {
    "fun": int(os.getenv('FUN_REDDIT')),
    "serious": int(os.getenv('SERIOUS_REDDIT')),
    "life": int(os.getenv('LIFE_REDDIT')),
}
blog_channels = {
    "company": int(os.getenv('COMPANY_BLOGS')),
    "individual": int(os.getenv('INDIVIDUAL_BLOGS')),
    "product": int(os.getenv('PRODUCT_BLOGS')),
    "infosec": int(os.getenv('INFOSEC_BLOGS')),
    "podcasts": int(os.getenv('PODCASTS')),
}
rant_channel = int(os.getenv('RANTS'))
forum_channel = int(os.getenv('FORUMS'))


async def _reddit_updater(frequency: str):
    logging.info('Running %s Reddit update', frequency)
    reddit_config = load_config('reddit.json')
    posts = reddit.get_reddit_posts(frequency, reddit_config['limit'])
    for subreddit in posts['subreddits']:
        for post in subreddit['posts']:
            embed = create_reddit_embed(subreddit, post)
            channel = bot.get_channel(reddit_channels[subreddit['category']])
            await channel.send(embed=embed)
            await asyncio.sleep(1)


async def _blog_updater(frequency: str):
    config = load_config('blogs.json')
    for blog in config.keys():
        logging.info('Running %s %s blog update', frequency, blog)
        blog_config = config[blog]
        if frequency == blog_config['frequency']:
            loop = asyncio.get_event_loop()
            posts = await loop.run_in_executor(
                ThreadPoolExecutor(),
                feeds.get_blog_posts,
                blog_config['data_file'],
                blog_config['limit_per_blog'],
                frequency
            )
            for post in posts:
                embed = create_blog_embed(post)
                channel = bot.get_channel(blog_channels[blog])
                await channel.send(embed=embed)
                await asyncio.sleep(1)


async def _devrant_updater(frequency: str):
    logging.info('Running %s devRant update', frequency)
    devrant_config = load_config('devrant.json')
    if frequency == devrant_config['frequency']:
        rants = devrant.get_rants(frequency, devrant_config['limit'])
        for rant in rants:
            embed = create_devrant_embed(rant)
            channel = bot.get_channel(int(rant_channel))
            await channel.send(embed=embed)
            await asyncio.sleep(1)


async def _forum_updater(frequency: str):
    config = load_config('forums.json')
    for forum in config.keys():
        logging.info('Running %s %s update', frequency, forum)
        forum_config = config[forum]
        if frequency == forum_config['frequency']:
            posts = forums.get_forum_posts(forum, forum_config['limit'])
            for post in posts:
                embed = create_forum_embed(forum, post)
                channel = bot.get_channel(int(forum_channel))
                await channel.send(embed=embed)
                await asyncio.sleep(1)


async def _update_posts(period):
    await _reddit_updater(period)
    await _blog_updater(period)
    await _devrant_updater(period)
    await _forum_updater(period)


async def _update_daily_posts():
    await _update_posts("daily")


bot = commands.Bot(command_prefix='./')


@bot.event
async def on_ready():
    '''
    Fired when bot is ready
    '''
    logging.info('Bot is ready!')
    await _update_daily_posts()

    exit()


bot.run(TOKEN)
