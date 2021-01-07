import os
import json
import discord
import random
import schedule

from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import date
from reddit import reddit

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
FUN = os.getenv('FUN')
WEBDEV = os.getenv('WEBDEV')
SYSAD = os.getenv('SYSADMIN')
ANDROID = os.getenv('ANDROID')
CAREER = os.getenv('CAREER')
BLOGS = os.getenv('BLOGS')
DEVRANT = os.getenv('DEVRANT')
SLASHDOT = os.getenv('ANDROID')

bot = commands.Bot(command_prefix='./')
jsonDict = reddit.result


def create_reddit_embed(subreddit_name, 
                        title, selftext, url, 
                        image_url, subreddit_url, 
                        subreddit_icon):
    if selftext == "":
        selftext = "\u200b"
    
    embed = discord.Embed(
        title = title,
        description = selftext,
        url = url,
        colour = discord.Colour.red()
    )

    if image_url != "":
        embed.set_image(url = image_url)

    embed.set_author(
        name = subreddit_name, 
        url = subreddit_url, 
        icon_url = subreddit_icon
        )

    return embed

@bot.event
async def on_ready():
    schedule.every().monday.do(reddit_weekly.start())
    schedule.every().day.at("00:00").do(reddit_daily.start())
    schedule.every().day.at("00:00").do(reddit_monthly.start())

@tasks.loop(hours=168)
async def reddit_weekly():
    for subreddit in jsonDict["subreddits"]:
        if subreddit["frequency"] == "weekly":
            if subreddit["subreddit_name"] == "webdev":
                channel = bot.get_channel(WEBDEV)
            elif subreddit["subreddit_name"] == "sysadmin":
                channel = bot.get_channel(SYSAD)
            elif subreddit["subreddit_name"] == "androiddev":
                channel = bot.get_channel(ANDROID)
            elif subreddit["subreddit_name"] == "ITCareerQuestions":
                channel = bot.get_channel(CAREER)
            else:
                channel = bot.get_channel(FUN)
            for post in subreddit["posts"]:
                embed = create_reddit_embed(subreddit["subreddit_name"],
                    post["title"], post["selftext"], post["url"], post["image"]["url"],
                    subreddit["subreddit_url"], subreddit["subreddit_icon"])
                await channel.send(embed = embed)
    
    return schedule.CancelJob

@tasks.loop(hours=168)
async def devrant():
    #fetch from devrant
    pass

@tasks.loop(hours=24)
async def reddit_monthly():
    if date.today().day != 1:
        return

    for subreddit in jsonDict["subreddits"]:
        if subreddit["frequency"] == "monthly":
            if subreddit["subreddit_name"] == "webdev":
                channel = bot.get_channel(WEBDEV)
            elif subreddit["subreddit_name"] == "sysadmin":
                channel = bot.get_channel(SYSAD)
            elif subreddit["subreddit_name"] == "androiddev":
                channel = bot.get_channel(ANDROID)
            elif subreddit["subreddit_name"] == "ITCareerQuestions":
                channel = bot.get_channel(CAREER)
            else:
                channel = bot.get_channel(FUN)
            for post in subreddit["posts"]:
                embed = create_reddit_embed(subreddit["subreddit_name"],
                    post["title"], post["selftext"], post["url"], post["image"]["url"],
                    subreddit["subreddit_url"], subreddit["subreddit_icon"])
                await channel.send(embed = embed)

    return schedule.CancelJob

@tasks.loop(hours=24)
async def reddit_daily():
    for subreddit in jsonDict["subreddits"]:
        if subreddit["frequency"] == "daily":
            if subreddit["subreddit_name"] == "webdev":
                channel = bot.get_channel(WEBDEV)
            elif subreddit["subreddit_name"] == "sysadmin":
                channel = bot.get_channel(SYSAD)
            elif subreddit["subreddit_name"] == "androiddev":
                channel = bot.get_channel(ANDROID)
            elif subreddit["subreddit_name"] == "ITCareerQuestions":
                channel = bot.get_channel(CAREER)
            else:
                channel = bot.get_channel(FUN)
            for post in subreddit["posts"]:
                embed = create_reddit_embed(subreddit["subreddit_name"],
                    post["title"], post["selftext"], post["url"], post["image"]["url"],
                    subreddit["subreddit_url"], subreddit["subreddit_icon"])
                await channel.send(embed = embed)
    
    return schedule.CancelJob

bot.run(TOKEN)