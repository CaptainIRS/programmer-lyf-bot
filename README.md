# Programmer Lyf Bot

[![lint](https://github.com/CaptainIRS/programmer-lyf-bot/actions/workflows/lint.yml/badge.svg)](https://github.com/CaptainIRS/programmer-lyf-bot/actions/workflows/lint.yml)
![](https://img.shields.io/github/license/CaptainIRS/programmer-lyf-bot)

This bot brings in the latest news, the latest tech, the latest memes, and everything needed to make a programmer's life complete.

> [!NOTE]
> The bot is alive in the following communities. Join the communities to get the latest updates every morning at 6AM IST from Programmer Lyf Bot:
> 
> [![Telegram-@ProgrammerLyf-blue](https://github.com/CaptainIRS/programmer-lyf-bot/assets/36656347/a5aa0750-6540-4cc8-a0de-b1df5612eea2)
](https://t.me/ProgrammerLyf)
> [![Discord-Programmer Lyf-blue](https://github.com/CaptainIRS/programmer-lyf-bot/assets/36656347/778bbe58-befe-44da-aef9-bd47b4215b9e)
](https://discord.gg/wMr5YBCCmv)

### Screenshots

| ![](https://i.imgur.com/DMg0lTt.png) | ![](https://i.imgur.com/1DPfeVg.png) | ![](https://i.imgur.com/UhZiX92.png) |
| --- | --- | --- |
| ![](https://i.imgur.com/r8hd7nb.png) | ![](https://i.imgur.com/ryFCEWe.png) | ![](https://i.imgur.com/VgYc7O0.png) |

### Development
1. Copy `.env.example` to `.env`
2. Fill out the required tokens in `.env`
3. Change the config files in `config/` as required
4. `python3 -m venv venv && source venv/bin/activate`
5. `pip3 install -r requirements-dev.txt`
6. `pre-commit install`
7. `python3 main.py daily` or `python3 main.py weekly`
