'''
Bot functions
'''

import asyncio
import logging
import os

import aioschedule as schedule
from discord.ext import commands
from dotenv import load_dotenv

import reddit
import blogs
import devrant
import forums

from util.load_config import load_config
from util.embed_utils import create_devrant_embed, create_reddit_embed, \
                                create_blog_embed, create_forum_embed

logging.basicConfig(level=logging.INFO)

load_dotenv(override=True)

TOKEN = os.getenv('DISCORD_TOKEN')

reddit_channels = {
    "fun": int(os.getenv('FUN')),
    "serious": int(os.getenv('WEBDEV')),
    "life": int(os.getenv('ANDROID')),
}
blog_channel = int(os.getenv('BLOGS'))
rant_channel = int(os.getenv('DEVRANT'))
forum_channel = int(os.getenv('FORUM'))


async def _reddit_updater(frequency: str):
    logging.info('Running %s Reddit update', frequency)
    reddit_config = load_config('reddit.json')
    posts = reddit.get_reddit_posts(frequency, reddit_config['limit'])
    for subreddit in posts['subreddits']:
        for post in subreddit['posts']:
            embed = create_reddit_embed(subreddit, post)
            channel = bot.get_channel(int(reddit_channels[subreddit['category']]))
            await channel.send(embed=embed)
            await asyncio.sleep(1)


async def _blog_updater(frequency: str):
    logging.info('Running %s blog update', frequency)
    async for posts in blogs.get_blog_posts():
        for post in posts:
            embed = create_blog_embed(post)
            channel = bot.get_channel(blog_channel)
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


async def _update_weekly_posts():
    await _update_posts("weekly")


async def start():
    '''
    Start running the scheduled tasks
    '''
    logging.info("Tasks have started running")
    schedule.every().day.at("00:00").do(_update_daily_posts)
    schedule.every().friday.at("02:00").do(_update_weekly_posts)

    while 1:
        await schedule.run_pending()
        await asyncio.sleep(1)


bot = commands.Bot(command_prefix='./')


@bot.event
async def on_ready():
    '''
    Fired when bot is ready
    '''
    logging.info('Bot is ready!')


bot.loop.create_task(start())

bot.run(TOKEN)
