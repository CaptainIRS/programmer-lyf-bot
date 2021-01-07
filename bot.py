import os
import json
import discord
import schedule
import devrant

from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import date, datetime
from reddit import reddit
from feeds import feeds

load_dotenv(override=True)

TOKEN = os.getenv('DISCORD_TOKEN')
FUN = int(os.getenv('FUN'))
WEBDEV = int(os.getenv('WEBDEV'))
SYSAD = int(os.getenv('SYSADMIN'))
ANDROID = int(os.getenv('ANDROID'))
CAREER = int(os.getenv('CAREER'))
BLOGS = int(os.getenv('BLOGS'))
DEVRANT = int(os.getenv('DEVRANT'))
SLASHDOT = int(os.getenv('ANDROID'))

bot = commands.Bot(command_prefix='./')
redditDict = reddit.result
blogDict = feeds.new_array

def create_reddit_embed(subreddit, 
                        title, selftext, url, image_type, 
                        image_url, subreddit_url, 
                        subreddit_icon):
    if selftext == "":
        selftext = "\u200b"

    if len(selftext) > 2044:
        selftext = selftext[:2044] + '...'
    
    embed = discord.Embed(
        title = title,
        description = selftext,
        url = url,
        colour = discord.Colour.red()
    )

    if image_url != "" and image_type == "image":
        embed.set_image(url = image_url)

    embed.set_author(
        name = subreddit, 
        url = subreddit_url, 
        icon_url = subreddit_icon
        )

    return embed

def create_blog_embed(author_name, title, description, url, image_url):
    if description == "":
        description = "\u200b"

    if len(description) > 2044:
        selftext = description[:2044] + '...'
    
    embed = discord.Embed(
        title = title,
        description = description,
        url = url,
        colour = discord.Colour.blue()
    )

    if image_url != "":
        embed.set_image(url = image_url)

    embed.set_author(name = author_name, icon_url = 'https://online.usm.edu/wp-content/uploads/2018/01/online-engineering-technology-blog-image.jpg')

    return embed

@bot.event
async def on_ready():
    reddit_weekly.start()
    reddit_daily.start()
    reddit_monthly.start()
    fetch_devrant.start()
    fetch_blog.start()

@tasks.loop(hours=24)
async def reddit_weekly():
    if datetime.today().weekday() != 0:
        return

    for subreddit in redditDict["subreddits"]:
        if subreddit["frequency"] == "weekly":
            if subreddit["subreddit"] == "webdev":
                channel = bot.get_channel(WEBDEV)
            elif subreddit["subreddit"] == "sysadmin":
                channel = bot.get_channel(SYSAD)
            elif subreddit["subreddit"] == "androiddev":
                channel = bot.get_channel(ANDROID)
            elif subreddit["subreddit"] == "ITCareerQuestions":
                channel = bot.get_channel(CAREER)
            else:
                channel = bot.get_channel(FUN)
            for post in subreddit["posts"]:
                embed = create_reddit_embed(subreddit["subreddit"],
                    post["title"], post["selftext"], post["url"], post["media"]["medium"], post["media"]["url"],
                    subreddit["subreddit_url"], subreddit["subreddit_icon"])
                try:
                    await channel.send(embed = embed)
                except:
                    pass
    

@tasks.loop(hours=24)
async def fetch_devrant():
    if datetime.today().weekday() != 0:
        return

    channel = bot.get_channel(DEVRANT)
    for embed in devrant.get_rants('weekly','10'):
        try:
            await channel.send(embed = embed)
        except:
            pass

@tasks.loop(hours=24)
async def reddit_monthly():
    if date.today().day != 1:
        return

    for subreddit in redditDict["subreddits"]:
        if subreddit["frequency"] == "monthly":
            if subreddit["subreddit"] == "webdev":
                channel = bot.get_channel(WEBDEV)
            elif subreddit["subreddit"] == "sysadmin":
                channel = bot.get_channel(SYSAD)
            elif subreddit["subreddit"] == "androiddev":
                channel = bot.get_channel(ANDROID)
            elif subreddit["subreddit"] == "ITCareerQuestions":
                channel = bot.get_channel(CAREER)
            else:
                channel = bot.get_channel(FUN)
            for post in subreddit["posts"]:
                embed = create_reddit_embed(subreddit["subreddit"],
                    post["title"], post["selftext"], post["url"], post["media"]["medium"], post["media"]["url"],
                    subreddit["subreddit_url"], subreddit["subreddit_icon"])
                try:
                    await channel.send(embed = embed)
                except:
                    pass


@tasks.loop(hours=1)
async def reddit_daily():
    if datetime.today().hour != 0:
        return

    for subreddit in redditDict["subreddits"]:
        if subreddit["frequency"] == "daily":
            if subreddit["subreddit"] == "webdev":
                channel = bot.get_channel(WEBDEV)
            elif subreddit["subreddit"] == "sysadmin":
                channel = bot.get_channel(SYSAD)
            elif subreddit["subreddit"] == "androiddev":
                channel = bot.get_channel(ANDROID)
            elif subreddit["subreddit"] == "ITCareerQuestions":
                channel = bot.get_channel(CAREER)
            else:
                channel = bot.get_channel(FUN)
            for post in subreddit["posts"]:
                embed = create_reddit_embed(subreddit["subreddit"],
                    post["title"], post["selftext"], post["url"], post["media"]["medium"], post["media"]["url"],
                    subreddit["subreddit_url"], subreddit["subreddit_icon"])
                try:
                    await channel.send(embed = embed)
                except:
                    pass
    
@tasks.loop(hours=1)
async def fetch_blog():
    if datetime.today().hour != 0:
        return

    channel = bot.get_channel(BLOGS)
    for post in blogDict:
        embed = create_blog_embed(post["author_name"],
                post["title"], post["description"], post["url"], post["image"],
                )
        try:
            await channel.send(embed = embed)
        except:
            pass

bot.run(TOKEN)