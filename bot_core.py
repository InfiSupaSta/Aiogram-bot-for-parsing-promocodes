import asyncio
import os
import json
import random

from aiogram import Bot, Dispatcher, executor, types

from keyboards import keyboard, keyboard_without_buttons
from env import set_env
from emojis_unicode import EMOJIS
from promo_parser import (get_response,
                          parse_and_save_current_promos_from_response_to_file,
                          handle_current_and_previous_check,
                          ROOT_PATH)

set_env()

bot = Bot(token=os.environ.get("BOT_TOKEN_API"))
dp = Dispatcher(bot, loop=asyncio.get_event_loop())


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
            promo_json = promo_file.read()
            promo_dict = json.loads(promo_json)
            promos_to_return = '\n'.join([f"`{promo.upper()}` \n{items} \nlink: http://withhive\.me/313/{promo}\n"
                                          for promo, items in promo_dict.items()])

        await call.message.answer(promos_to_return,
                                  parse_mode=types.ParseMode.MARKDOWN_V2,
                                  disable_web_page_preview=True)

    await call.message.edit_text(text="Button is clicked, parsing actual promocodes... Here they are \U00002b07\n"
                                      "You can click on promo to copy it on clipboard! "
                                      f"{random.randint(2, 5) * EMOJIS.get('star')}",
                                 reply_markup=keyboard_without_buttons)


async def check_new_promo():
    while True:
        response = get_response(os.getenv("COM2US_URL_WITH_PROMO"))
        parse_and_save_current_promos_from_response_to_file(response).items()

        await handle_current_and_previous_check(f"{ROOT_PATH}/promocodes/previous_check",
                                                f"{ROOT_PATH}/promocodes/current_check",
                                                bot,
                                                int(os.getenv("CHAT_ID")))
        await asyncio.sleep(600)


async def check_if_user_already_in_db(user_id: int, username: str) -> None:
    path_to_file_with_users_id = f"{ROOT_PATH}/subbed_users"

    if not os.path.exists(path_to_file_with_users_id):
        with open(path_to_file_with_users_id, "w") as users_id:
            users_id.write('{}')

    with open(path_to_file_with_users_id, "r") as file_with_users_id:
        users = file_with_users_id.read()

    json_to_dict = await json.loads(users)
    if user_id not in json_to_dict.keys():
        json_to_dict[str(user_id)] = str(username)
    try:
        with open(path_to_file_with_users_id, "r+") as file_with_users_id:
            file_with_users_id.write(json.dumps(json_to_dict))
    except Exception as exception:
        print(">>> users", users)  # need logging here
        print(">>> exception", exception)  # need logging here


if __name__ == '__main__':
    dp.loop.create_task(check_new_promo())
    executor.start_polling(dp, skip_updates=False)
