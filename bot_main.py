import json
import random

from aiogram.utils import executor
from aiogram import types

from bot_initializer import dp
from coroutines import check_new_promo, check_if_user_already_in_db
from emojis_unicode import EMOJIS
from keyboards import keyboard, keyboard_without_buttons
from promo_parser import ROOT_PATH
from logger.core import create_logger

logger = create_logger("bot_errors_logger")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Hello, fellow summoner! This bot will inform you about new "
                        "Summoners War promocodes - it will "
                        "be send automatically when new promo appears. "
                        "To see actual promocodes use /get_actual_promo command.")


@dp.message_handler(commands=['get_actual_promo'])
async def process_start_command(message: types.Message):
    await message.reply("Hello, fellow summoner! Click the button below to see actual promocodes!",
                        reply_markup=keyboard)


@dp.message_handler()
async def wrong_command_reply_and_new_users_add(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await check_if_user_already_in_db(user_id, username)
    await message.reply("Please use /help or /get_actual_promo commands. \U00002764")


@dp.callback_query_handler(text_contains='promo')
async def return_promo_with_inline_button(call: types.CallbackQuery):
    if call.data and call.data == "promo":
        with open(f"{ROOT_PATH}/promocodes/current_check", "r") as promo_file:
            promo_json: str = promo_file.read()
            promo_dict: dict = json.loads(promo_json)
            promos_to_return: str = '\n'.join([f"`{promo.upper()}` \n{items} \nLINK: http://withhive\.me/313/{promo}\n"
                                               for promo, items in promo_dict.items()])

        await call.message.answer(promos_to_return,
                                  parse_mode=types.ParseMode.MARKDOWN_V2,
                                  disable_web_page_preview=True)

    await call.message.edit_text(text="Button is clicked, parsing actual promocodes... Here they are \U00002b07\n"
                                      "You can click on promo to copy it on clipboard! "
                                      f"{random.randint(2, 5) * EMOJIS.get('star')}",
                                 reply_markup=keyboard_without_buttons)


if __name__ == '__main__':
    dp.loop.create_task(check_new_promo())
    executor.start_polling(dp, skip_updates=False)
