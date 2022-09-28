import asyncio
import json
import os

from bot_initializer import bot
from promo_parser import (ROOT_PATH,
                          parse_and_save_current_promos_from_response_to_file,
                          handle_current_and_previous_check,
                          get_response)
from logger.core import create_logger

logger = create_logger("bot_errors_logger")


async def check_new_promo():
    while True:
        response = get_response(os.getenv("COM2US_URL_WITH_PROMO"))

        if response == '':
            continue

        parse_and_save_current_promos_from_response_to_file(response).items()

        await handle_current_and_previous_check(f"{ROOT_PATH}/promocodes/previous_check",
                                                f"{ROOT_PATH}/promocodes/current_check",
                                                bot)
        await asyncio.sleep(600)


async def check_if_user_already_in_db(user_id: int, username: str) -> None:
    path_to_file_with_users_id = f"{ROOT_PATH}/subbed_users"

    if not os.path.exists(path_to_file_with_users_id):
        with open(path_to_file_with_users_id, "w") as users_id:
            users_id.write('{}')

    with open(path_to_file_with_users_id, "r") as file_with_users_id:
        users = file_with_users_id.read()

    json_to_dict = json.loads(users)
    if user_id not in json_to_dict.keys():
        json_to_dict[str(user_id)] = str(username)
    try:
        with open(path_to_file_with_users_id, "r+") as file_with_users_id:
            file_with_users_id.write(json.dumps(json_to_dict))
    except Exception as exception:
        logger.error(f"Error occurred while checking user exists in db. "
                     f"Users: {users}. User_id: {user_id}. Error: {str(exception)}")
