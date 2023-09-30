# Programmer Lyf Bot

[![lint](https://github.com/CaptainIRS/programmer-lyf-bot/actions/workflows/lint.yml/badge.svg)](https://github.com/CaptainIRS/programmer-lyf-bot/actions/workflows/lint.yml)
![](https://img.shields.io/github/license/CaptainIRS/programmer-lyf-bot)

This bot brings in the latest news, the latest tech, the latest memes, and everything needed to make a programmer's life complete.

> [!NOTE]
> Join the communities to get the latest updates and to suggest new features:
> [![Telegram](https://img.shields.io/badge/Telegram-%40ProgrammerLyf-blue?logo=telegram)](https://t.me/ProgrammerLyf)
> [![Discord](https://img.shields.io/badge/Discord-Programmer%20Lyf-blue?logo=discord)](https://discord.gg/wMr5YBCCmv)

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
