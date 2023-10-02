# Contributing

The repo is open to contributions. Contributions can be made in the form of:
* No-code contributions
  * [Finding and adding new feeds](#adding-new-feeds)
* Code contributions. (See [Setting up the development environment](#setting-up-the-development-environment) for instructions on setting up the development environment.)
  * Adding new features
  * Improving existing features
  * Improving the codebase

## Adding new feeds

1. Check out sites like [Hacker News](https://news.ycombinator.com/) and [Medium](https://medium.com/) for new blogs. Find blogs that are relevant to the bot, which is anything related to programming, possibly popular ones.
2. Check out the files in the [data/blogs](./data/blogs) directory. The files are named after the category of the blogs they contain. For example, [data/blogs/company_blogs.opml](./data/blogs/company_blogs.opml) contains the list of company blogs. Check if the blog you found is already present in any of the files.
3. If the blog is not present in any of the files, find the RSS feed of the blog by following the steps below:
    1. Open the blog in a browser.
    2. Right click on the page and click on `View Page Source`.
    3. Use `Ctrl + F` or `Cmd + F` (In MacOS) to search for `rss` or `feed`.
    4. If you find a link has the word `feed` in it and/or ends with `.xml`, copy the link and paste it in a new tab.
    5. If the page that opens contains a list of posts, then you have found the feed. If not, the blog does not have a feed and unfortunately cannot be added to the bot. (You can try contacting the blog owner and asking them to add a feed.)
4. Open the file in the [data/blogs](./data/blogs) directory that is relevant to the blog you found. For example, if you found a company blog, open [data/blogs/company_blogs.opml](./data/blogs/company_blogs.opml).
6. Click on the edit button on the top right corner of the file. It looks like a pencil.
5. You will see multiple lines like `<outline type="rss" ... />`. Duplicate one of the lines and edit the attributes as follows:
    * `title`: The title of the blog.
    * `text`: One-line description of the blog. (Optional)
    * `xmlUrl`: The URL of the feed you found in step 3.
    * `htmlUrl`: The URL of the blog you found in step 1.
7. Click on the `Commit changes` button near the top-right corner of the page. Add a commit message like `Add <blog name>`. You can also add a description describing where you found the blog and why you think it is relevant to the bot. Then click on the `Propose changes` button.
8. A new page will open. Add a title and description for the pull request and click on the `Create pull request` button.


## Setting up the development environment
0. Install Python 3.9 or higher
1. Copy `.env.example` to `.env`
2. Fill out the required tokens in `.env`
    1. Telegram specific can be obtained by creating a bot by following [these instructions](https://core.telegram.org/bots/features#creating-a-new-bot)
    2. Discord specific can be obtained by creating a bot by following [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html)
3. Change the config files in `config/` as required
4. `python3 -m venv venv && source venv/bin/activate`
5. `pip3 install -r requirements-dev.txt`
6. `pre-commit install`

### Running the bot
Run the commands `python3 main.py daily` or `python3 main.py weekly` to run the bot in daily or weekly mode respectively.
