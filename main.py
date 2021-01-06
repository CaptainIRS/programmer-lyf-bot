'''
Bot functions
'''

import asyncio
import base64
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import discord
from discord.ext import commands
from dotenv import load_dotenv

import devrant
import feeds
import forums
import reddit
from util.embed_utils import (create_blog_embed, create_devrant_embed,
                              create_forum_embed, create_reddit_embed)
from util.load_config import load_config

logging.basicConfig(level=logging.INFO)

load_dotenv(override=True)

TOKEN = os.getenv('DISCORD_TOKEN')

reddit_channels = {
    'fun': int(os.getenv('FUN_REDDIT')),
    'serious': int(os.getenv('SERIOUS_REDDIT')),
    'life': int(os.getenv('LIFE_REDDIT')),
}
blog_channels = {
    'company': int(os.getenv('COMPANY_BLOGS')),
    'individual': int(os.getenv('INDIVIDUAL_BLOGS')),
    'product': int(os.getenv('PRODUCT_BLOGS')),
    'infosec': int(os.getenv('INFOSEC_BLOGS')),
    'podcasts': int(os.getenv('PODCASTS')),
}
rant_channel = int(os.getenv('RANTS'))
forum_channel = int(os.getenv('FORUMS'))
debug_channel = int(os.getenv('DEBUG_CHANNEL'))


class ProgrammerLyfBot(commands.Bot):
    '''
    Wrapper class around the Discord bot class
    '''

    def __init__(self, period, *args, **kwargs):
        self.period = period
        super().__init__(*args, **kwargs)

    async def _reddit_updater(self, frequency: str):
        logging.info('Running %s Reddit update', frequency)
        reddit_config = load_config('reddit.json')
        posts = reddit.get_reddit_posts(frequency, reddit_config['limit'])
        for subreddit in posts['subreddits']:
            for post in subreddit['posts']:
                embed = create_reddit_embed(subreddit, post)
                channel = self.get_channel(reddit_channels[subreddit['category']])
                await channel.send(embed=embed)
                await asyncio.sleep(0.1)

    async def _blog_updater(self, frequency: str):
        config = load_config('blogs.json')
        for blog in config.keys():
            logging.info('Running %s %s blog update', frequency, blog)
            blog_config = config[blog]
            if frequency == blog_config['frequency']:
                loop = asyncio.get_event_loop()
                posts = await loop.run_in_executor(
                    ThreadPoolExecutor(),
                    feeds.get_feed,
                    blog_config['data_file'],
                    blog_config['limit_per_blog'],
                    frequency
                )
                for post in posts:
                    embed = create_blog_embed(post)
                    channel = self.get_channel(blog_channels[blog])
                    await channel.send(embed=embed)
                    await asyncio.sleep(0.1)

    async def _devrant_updater(self, frequency: str):
        logging.info('Running %s devRant update', frequency)
        devrant_config = load_config('devrant.json')
        if frequency == devrant_config['frequency']:
            rants = devrant.get_rants(frequency, devrant_config['limit'])
            for rant in rants:
                embed = create_devrant_embed(rant)
                channel = self.get_channel(int(rant_channel))
                await channel.send(embed=embed)
                await asyncio.sleep(0.1)

    async def _forum_updater(self, frequency: str):
        config = load_config('forums.json')
        for forum in config.keys():
            logging.info('Running %s %s update', frequency, forum)
            forum_config = config[forum]
            if frequency == forum_config['frequency']:
                posts = forums.get_forum_posts(forum, forum_config['limit'])
                for post in posts:
                    embed = create_forum_embed(forum, post)
                    channel = self.get_channel(int(forum_channel))
                    await channel.send(embed=embed)
                    await asyncio.sleep(0.1)

    async def update_posts(self, period):
        '''
        Fetch and update posts in respective channels
        '''
        await self._reddit_updater(period)
        await self._blog_updater(period)
        await self._devrant_updater(period)
        await self._forum_updater(period)

    async def on_ready(self):
        '''
        Fired when bot is ready
        '''
        logging.info('Bot is ready!')
        await self.update_posts(self.period)
        channel = self.get_channel(int(debug_channel))
        await channel.send(file=discord.File('/tmp/debug.log'))
        await self.logout()
        sys.exit()

    async def on_error(self, event_method, *args, **kwargs):
        await super().on_error(event_method, *args, **kwargs)
        await self.logout()
        sys.exit()


def _run_bot_in_thread(frequency: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = ProgrammerLyfBot(frequency, command_prefix='./')
    loop.run_until_complete(bot.start(TOKEN))


def cloud_function_entrypoint(event: dict[str, str], _):
    '''
    Entrypoint for Google Cloud Function trigger
    '''
    frequency = base64.b64decode(event['data']).decode('utf-8')
    bot_thread = Thread(target=_run_bot_in_thread, args=(frequency,))
    bot_thread.start()
    bot_thread.join()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments. Usage: python3 main.py weekly|daily')
        sys.exit()
    if sys.argv[1] == 'weekly':
        thread = Thread(target=_run_bot_in_thread, args=('weekly',))
    elif sys.argv[1] == 'daily':
        thread = Thread(target=_run_bot_in_thread, args=('daily',))
    thread.start()
    thread.join()
