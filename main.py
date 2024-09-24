'''
Bot functions
'''

import asyncio
import logging
import os
import sys
from multiprocessing import JoinableQueue, Process
from time import sleep

import discord
import simplematrixbotlib as botlib
import telegram
from discord.ext import commands
from dotenv import load_dotenv
from praw import Reddit

import feeds
import forums
import reddit
from util.embed_utils import (RedditPost, TelegramPost, create_blog_embed,
                              create_blog_matrix_post, create_blog_reddit_post,
                              create_blog_telegram_post, create_forum_embed,
                              create_forum_matrix_post,
                              create_forum_reddit_post,
                              create_forum_telegram_post, create_reddit_embed,
                              create_reddit_matrix_post,
                              create_reddit_telegram_post)
from util.load_config import load_config

logging.basicConfig(level=logging.INFO)

load_dotenv(override=True)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
REDDIT_SUBREDDIT = os.getenv('REDDIT_SUBREDDIT')

discord_channels = {
    'reddit': {
        'fun': int(os.getenv('DISCORD_FUN_REDDIT')),
        'serious': int(os.getenv('DISCORD_SERIOUS_REDDIT')),
        'life': int(os.getenv('DISCORD_LIFE_REDDIT')),
    },
    'blog': {
        'company': int(os.getenv('DISCORD_COMPANY_BLOGS')),
        'product': int(os.getenv('DISCORD_PRODUCT_BLOGS')),
        'infosec': int(os.getenv('DISCORD_INFOSEC_BLOGS')),
        'news': int(os.getenv('DISCORD_NEWS')),
        'individual': int(os.getenv('DISCORD_INDIVIDUAL_BLOGS')),
    },
    'forum': int(os.getenv('DISCORD_FORUMS')),
    'debug': int(os.getenv('DISCORD_DEBUG_CHANNEL')),
}

telegram_threads = {
    'reddit': {
        'fun': int(os.getenv('TELEGRAM_FUN_REDDIT')),
        'serious': int(os.getenv('TELEGRAM_SERIOUS_REDDIT')),
        'life': int(os.getenv('TELEGRAM_LIFE_REDDIT')),
    },
    'blog': {
        'company': int(os.getenv('TELEGRAM_COMPANY_BLOGS')),
        'product': int(os.getenv('TELEGRAM_PRODUCT_BLOGS')),
        'infosec': int(os.getenv('TELEGRAM_INFOSEC_BLOGS')),
        'news': int(os.getenv('TELEGRAM_NEWS')),
        'individual': int(os.getenv('TELEGRAM_INDIVIDUAL_BLOGS')),
    },
    'forum': int(os.getenv('TELEGRAM_FORUMS')),
}

reddit_flairs = {
    'blog': {
        'company': os.getenv('REDDIT_COMPANY_BLOGS'),
        'product': os.getenv('REDDIT_PRODUCT_BLOGS'),
        'infosec': os.getenv('REDDIT_INFOSEC_BLOGS'),
        'news': os.getenv('REDDIT_NEWS'),
    },
    'forum': os.getenv('REDDIT_FORUMS'),
}

matrix_space = os.getenv('MATRIX_SPACE')
matrix_rooms = {
    'reddit': {
        'fun': os.getenv('MATRIX_FUN_REDDIT'),
        'serious': os.getenv('MATRIX_SERIOUS_REDDIT'),
        'life': os.getenv('MATRIX_LIFE_REDDIT'),
    },
    'blog': {
        'company': os.getenv('MATRIX_COMPANY_BLOGS'),
        'product': os.getenv('MATRIX_PRODUCT_BLOGS'),
        'infosec': os.getenv('MATRIX_INFOSEC_BLOGS'),
        'news': os.getenv('MATRIX_NEWS'),
        'individual': os.getenv('MATRIX_INDIVIDUAL_BLOGS'),
    },
    'forum': os.getenv('MATRIX_FORUMS'),
}


class Updater:  # pylint: disable=too-few-public-methods
    '''
    Puts post updates in queue
    '''

    def __init__(self, frequency: str, queue: JoinableQueue):
        self.frequency = frequency
        self.queue = queue

    def _reddit_updater(self):
        logging.info('Running %s Reddit update', self.frequency)
        reddit_config = load_config('reddit.json')
        posts = reddit.get_reddit_posts(self.frequency, reddit_config['limit'])
        for subreddit in posts['subreddits']:
            for post in subreddit['posts']:
                self.queue.put(('reddit', subreddit, post))

    def _blog_updater(self):
        config = load_config('blogs.json')
        for blog in config.keys():
            logging.info('Running %s %s blog update', self.frequency, blog)
            blog_config = config[blog]
            if self.frequency == blog_config['frequency']:
                feeds.submit_updates(
                    self.queue,
                    blog,
                    blog_config['data_file'],
                    blog_config['limit_per_blog'],
                    self.frequency
                )

    def _forum_updater(self):
        config = load_config('forums.json')
        for forum in config.keys():
            logging.info('Running %s %s update', self.frequency, forum)
            forum_config = config[forum]
            if self.frequency == forum_config['frequency']:
                posts = forums.get_forum_posts(forum, forum_config['limit'])
                for post in posts:
                    self.queue.put(('forum', forum, post))

    def update_posts(self):
        '''
        Fetch and update posts in respective channels
        '''
        self._reddit_updater()
        self._blog_updater()
        self._forum_updater()
        self.queue.put(None)


class DiscordBot(commands.Bot):
    '''
    Discord bot
    '''

    def __init__(self, command_prefix: str, queue: JoinableQueue):
        self.queue = queue
        intents = discord.Intents.default()
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        '''
        Fired when bot is ready
        '''
        logging.info('Bot is ready!')
        while True:
            message = self.queue.get()
            if message is None:
                self.queue.task_done()
                break
            source, channel, post = message
            if source == 'reddit':
                embed = create_reddit_embed(channel, post)
                await self.send_embed(discord_channels['reddit'][channel['category']], embed)
            elif source == 'blog':
                embed = create_blog_embed(post)
                await self.send_embed(discord_channels['blog'][channel], embed)
            elif source == 'forum':
                embed = create_forum_embed(channel, post)
                await self.send_embed(discord_channels['forum'], embed)
            self.queue.task_done()
            await asyncio.sleep(3)
        channel = self.get_channel(discord_channels['debug'])
        await channel.send(file=discord.File('/tmp/debug.log'))
        await self.logout()

    async def send_embed(self, channel_id: int, embed: discord.Embed):
        '''
        Send embed to channel
        '''
        await self.wait_until_ready()
        channel = self.get_channel(channel_id)
        try:
            await channel.send(embed=embed)
        except Exception as exception:  # pylint: disable=broad-except
            logging.error('Error sending message %s to discord: %s', embed.to_dict()['title'], exception)

    async def on_error(self, event_method, *args, **kwargs):
        await super().on_error(event_method, *args, **kwargs)
        await self.logout()


def run_discord_bot(queue: JoinableQueue):
    '''
    Run discord bot
    '''
    discord_bot = DiscordBot(command_prefix='./', queue=queue)
    discord_bot.run(DISCORD_TOKEN)


def run_matrix_bot(queue: JoinableQueue):
    '''
    Run matrix bot
    '''
    creds = botlib.Creds(
        os.getenv('MATRIX_HOMESERVER'),
        os.getenv('MATRIX_USER'),
        access_token=os.getenv('MATRIX_TOKEN'))
    bot = botlib.Bot(creds)

    @bot.listener.on_startup
    async def on_startup(room_id: str):
        if room_id != matrix_space:
            return
        while True:
            message = queue.get()
            if message is None:
                queue.task_done()
                break
            source, channel, post = message
            if source == 'reddit':
                matrix_post = create_reddit_matrix_post(channel, post)
                await bot.api.send_markdown_message(
                    room_id=matrix_rooms['reddit'][channel['category']],
                    message=matrix_post.markdown)
            elif source == 'blog':
                matrix_post = create_blog_matrix_post(post)
                await bot.api.send_markdown_message(
                    room_id=matrix_rooms['blog'][channel],
                    message=matrix_post.markdown)
            elif source == 'forum':
                matrix_post = create_forum_matrix_post(channel, post)
                await bot.api.send_markdown_message(
                    room_id=matrix_rooms['forum'],
                    message=matrix_post.markdown)
            queue.task_done()
            await asyncio.sleep(1)
        await bot.async_client.logout()
    bot.run()


async def send_to_telegram_channel(telegram_bot: telegram.Bot, thread_id: str, post: TelegramPost):
    '''
    Send message to telegram channel
    '''
    try:
        if post.image_url:
            await telegram_bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=post.image_url,
                caption=len(post.message) > 1024 and f'{post.message[:1000]}[...]' or post.message,
                parse_mode=telegram.constants.ParseMode.HTML,
                disable_notification=True,
                message_thread_id=thread_id,
            )
        else:
            await telegram_bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=post.message,
                parse_mode=telegram.constants.ParseMode.HTML,
                disable_web_page_preview=not post.show_preview,
                disable_notification=True,
                message_thread_id=thread_id,
            )
    except Exception as exception:  # pylint: disable=broad-except
        logging.error('Error sending message %s to telegram: %s', post.message, exception)


async def send_telegram_messages(queue: JoinableQueue, telegram_bot: telegram.Bot):
    '''
    Send messages to telegram
    '''
    async with telegram_bot:
        while True:
            message = queue.get()
            if message is None:
                queue.task_done()
                break
            source, channel, post = message
            if source == 'reddit':
                telegram_post = create_reddit_telegram_post(channel, post)
                await send_to_telegram_channel(
                    telegram_bot,
                    telegram_threads['reddit'][channel['category']],
                    telegram_post
                )
            elif source == 'blog':
                telegram_post = create_blog_telegram_post(post)
                await send_to_telegram_channel(telegram_bot, telegram_threads['blog'][channel], telegram_post)
            elif source == 'forum':
                telegram_post = create_forum_telegram_post(channel, post)
                await send_to_telegram_channel(telegram_bot, telegram_threads['forum'], telegram_post)
            queue.task_done()
            await asyncio.sleep(3)


def run_telegram_bot(queue: JoinableQueue):
    '''
    Run telegram bot
    '''
    telegram_bot = telegram.Bot(TELEGRAM_TOKEN)
    asyncio.run(send_telegram_messages(queue, telegram_bot))


def send_to_subreddit(reddit_client: Reddit, flair_id: str, post: RedditPost):
    '''
    Send message to subreddit
    '''
    try:
        if post.url:
            reddit_client.subreddit(REDDIT_SUBREDDIT).submit(
                title=post.title,
                url=post.url,
                flair_id=flair_id,
                send_replies=False,
            )
        else:
            reddit_client.subreddit(REDDIT_SUBREDDIT).submit(
                title=post.title,
                selftext=post.description,
                flair_id=flair_id,
                send_replies=False,
            )
    except Exception as exception:  # pylint: disable=broad-except
        logging.error('Error sending message %s to reddit: %s', post.title, exception)


def run_reddit_bot(queue: JoinableQueue):
    '''
    Run reddit bot
    '''
    reddit_client = reddit.get_reddit_client()

    while True:
        message = queue.get()
        if message is None:
            queue.task_done()
            break
        source, channel, post = message
        if source == 'reddit':
            queue.task_done()
            continue
        if source == 'blog':
            reddit_post = create_blog_reddit_post(post)
            flair = reddit_flairs['blog'][channel]
            send_to_subreddit(reddit_client, flair, reddit_post)
        elif source == 'forum':
            reddit_post = create_forum_reddit_post(channel, post)
            flair = reddit_flairs['forum']
            send_to_subreddit(reddit_client, flair, reddit_post)
        queue.task_done()
        sleep(1)


def message_sender(message_queue: JoinableQueue):
    '''
    Send messages to the respective platforms
    '''
    queues = []
    if DISCORD_TOKEN:
        logging.info('Starting discord bot')
        discord_queue = JoinableQueue()
        queues.append(discord_queue)
        discord_process = Process(target=run_discord_bot, args=(discord_queue,))
        discord_process.start()
    if TELEGRAM_TOKEN:
        logging.info('Starting telegram bot')
        telegram_queue = JoinableQueue()
        queues.append(telegram_queue)
        telegram_process = Process(target=run_telegram_bot, args=(telegram_queue,))
        telegram_process.start()
    if REDDIT_SUBREDDIT:
        logging.info('Starting reddit bot')
        reddit_queue = JoinableQueue()
        queues.append(reddit_queue)
        reddit_process = Process(target=run_reddit_bot, args=(reddit_queue,))
        reddit_process.start()
    if os.getenv('MATRIX_USER') and os.getenv('MATRIX_TOKEN'):
        logging.info('Starting matrix bot')
        matrix_queue = JoinableQueue()
        queues.append(matrix_queue)
        matrix_process = Process(target=run_matrix_bot, args=(matrix_queue,))
        matrix_process.start()
    while True:
        message = message_queue.get()
        if message is None:
            message_queue.task_done()
            break
        for queue in queues:
            queue.put(message)
        message_queue.task_done()
    for queue in queues:
        queue.put(None)
    for queue in queues:
        queue.join()


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ['daily', 'weekly']:
        print('Invalid arguments. Usage: python3 main.py weekly|daily')
        sys.exit()
    post_queue = JoinableQueue()
    updater_process = Process(target=Updater(sys.argv[1], post_queue).update_posts)
    sender_process = Process(target=message_sender, args=(post_queue,))
    updater_process.start()
    sender_process.start()
    updater_process.join()
    post_queue.join()
