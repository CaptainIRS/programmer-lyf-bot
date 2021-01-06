# Programmer Lyf Bot

[![lint](https://github.com/CaptainIRS/programmer-lyf-bot/actions/workflows/lint.yml/badge.svg)](https://github.com/CaptainIRS/programmer-lyf-bot/actions/workflows/lint.yml)
![](https://img.shields.io/github/license/CaptainIRS/programmer-lyf-bot)

This bot brings in the latest news, the latest memes, the latest rants and everything needed to make a programmer's life complete

### Screenshots

| ![](https://i.imgur.com/lNFQ9IC.png) | ![](https://i.imgur.com/Lm26WaH.png) | ![](https://i.imgur.com/oyFpqlT.png) |
| --- | --- | --- |
| ![](https://i.imgur.com/gCLUH45.png) | ![](https://i.imgur.com/7dAxim7.png) | ![](https://i.imgur.com/THUHhyI.png) |

### Development
1. Copy `.env.example` to `.env`
2. Fill out the required tokens in `.env`
3. Change the config files in `config/` as required
4. `python3 -m venv venv && source venv/bin/activate`
5. `pip3 install -r requirements-dev.txt`
6. `pre-commit install`
7. `python3 main.py daily` or `python3 main.py weekly`
