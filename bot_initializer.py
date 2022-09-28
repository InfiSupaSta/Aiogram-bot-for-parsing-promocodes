import asyncio
import os

from aiogram import Bot, Dispatcher

from env import set_env

set_env()

bot = Bot(token=os.environ.get("BOT_TOKEN_API"))
dp = Dispatcher(bot, loop=asyncio.get_event_loop())
