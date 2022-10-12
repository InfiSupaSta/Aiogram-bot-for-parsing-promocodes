import asyncio
import json
import os

import aiohttp

from bot_initializer import bot
from promo_parser import (ROOT_PATH,
                          parse_and_save_current_promos_from_response_to_file,
                          handle_current_and_previous_check)
from logger.core import create_logger

error_logger = create_logger("bot_errors_logger")
new_user_logger = create_logger("new_user_logger")


class Response:
    """
    Class for getting async response text from a single URL.
    """

    def __init__(self, url: str = os.environ.get("COM2US_URL_WITH_PROMO")):
        self.url = url

    async def get_response(self, client):
        async with client.get(self.url) as response:
            if response.status != 200:
                await asyncio.sleep(10)
                return await self.get_response(client)

            return await response.text()

    async def main(self):
        async with aiohttp.ClientSession() as client:
            return await self.get_response(client)


async def check_new_promo():
    while True:
        response = await Response().main()
        parse_and_save_current_promos_from_response_to_file(response).items()

        path_to_file_with_previous_promo_check = f"{ROOT_PATH}/promocodes/previous_check"
        path_to_file_with_current_promo_check = f"{ROOT_PATH}/promocodes/current_check"

        await handle_current_and_previous_check(path_to_file_with_previous_promo_check,
                                                path_to_file_with_current_promo_check,
                                                bot)
        await asyncio.sleep(600)


async def check_if_user_already_in_db(user_id: int,
                                      username: str,
                                      file_with_users_id: str = "subbed_users") -> None:
    path_to_file_with_users_id = f"{ROOT_PATH}/{file_with_users_id}"

    if not os.path.exists(path_to_file_with_users_id):
        with open(path_to_file_with_users_id, "w") as users_id:
            users_id.write('{}')

    with open(path_to_file_with_users_id, "r") as file_with_users_id:
        users = file_with_users_id.read()

    json_to_dict = json.loads(users)

    if str(user_id) in json_to_dict.keys():
        return

    json_to_dict[str(user_id)] = str(username)
    try:
        with open(path_to_file_with_users_id, "r+") as file_with_users_id:
            file_with_users_id.write(json.dumps(json_to_dict))
        new_user_logger.info(f"New user join the bot, id: {user_id}, username: {username}")
    except Exception as exception:
        error_logger.error(f"Error occurred while checking user exists in db. "
                           f"Users: {users}. User_id: {user_id}. Error: {str(exception)}")
