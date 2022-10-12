import asyncio
import os

from aiogram import Bot, Dispatcher

from env import set_env

set_env()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

bot = Bot(token=os.environ.get("BOT_TOKEN_API"))
dp = Dispatcher(bot, loop=loop)
