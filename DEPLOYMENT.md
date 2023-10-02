# Deploying

## Setting up GitHub Actions
* Fork this repository
* Go to `Settings` > `Secrets and variables` > `Actions` > `New repository secret`
* Create a variable named `ENV_FILE` and paste the contents of [`.env.example`](./.env.example) in the value field
* Fill out the required tokens in `.env`
    * Telegram specific can be obtained by creating a bot by following [these instructions](https://core.telegram.org/bots/features#creating-a-new-bot)
    * Discord specific can be obtained by creating a bot by following [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html)
* Change the config files in `config/` as required
* Change the workflow files in `.github/workflows/` to add the cron schedule you want like:
  * For daily updates: `0 0 * * *`, for weekly updates: `0 0 * * 0`
    ```yaml
    on:
      schedule:
        - cron: '0 0 * * *'
    ```
