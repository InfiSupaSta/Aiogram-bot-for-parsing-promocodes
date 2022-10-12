import json
import pathlib
from os.path import exists
from os import mkdir

import aiogram

from logger.core import create_logger

logger = create_logger("bot_errors_logger")

ROOT_PATH = pathlib.Path(__file__).parent


def check_promocode_folder_exists() -> None:
    if not exists(f"{ROOT_PATH}/promocodes"):
        mkdir(f"{ROOT_PATH}/promocodes")


def parse_and_save_current_promos_from_response_to_file(response_text: str) -> dict[str, str]:
    response_from_json_to_dict = json.loads(response_text)
    active_coupons = dict()

    check_promocode_folder_exists()

    for coupon in response_from_json_to_dict.get("data"):
        items_in_promo = ""
        if coupon.get('Status') != "verified":
            continue
        for resource in coupon.get("Resources"):
            items_in_promo += f"{resource.get('Quantity')} {resource.get('Sw_Resource').get('Label')}; "
        active_coupons[coupon.get("Label")] = items_in_promo.rstrip("; ")

    with open(f"{ROOT_PATH}/promocodes/current_check", "w") as file_with_promo:
        dict_to_json = json.dumps(active_coupons)
        file_with_promo.write(dict_to_json)

    return active_coupons


async def handle_current_and_previous_check(path_to_file_with_previous_check: str,
                                            path_to_file_with_current_check: str,
                                            bot: aiogram.Bot) -> None:
    """
    Compare two files with promocodes - current and previous revisions. If new promo will be found
    in new active (not expired) codes from request, it will be sent in chat automatically for users,
    that at least once interacted with bot.
    :param path_to_file_with_previous_check:
    :param path_to_file_with_current_check:
    :param bot: instance of current bot
    :return: None
    """

    for path_to_file in [path_to_file_with_current_check, path_to_file_with_previous_check]:
        if not exists(path_to_file):
            open(path_to_file, "w")

    with open(path_to_file_with_current_check) as current, open(path_to_file_with_previous_check) as previous:
        current_check_data: str = current.read()
        previous_check_data: str = previous.read()

    if not previous_check_data:
        previous_check_data: str = '{"promo": "does not found"}'

    current_promo: dict = json.loads(current_check_data)
    previous_promo: dict = json.loads(previous_check_data)

    with open(f"{ROOT_PATH}/subbed_users") as users_id:
        users: dict = json.loads(users_id.read())

    for promocode in current_promo.keys():
        if previous_promo.get(promocode) is not None:
            continue

        items = current_promo.get(promocode)

        # message edited according to markdown v2
        message_to_send = "*NEW PROMO\!* \(click on promo below to save it ot clipboard\)\n\n" \
                          f"\>\>\> `{promocode.upper()}` \<\<\< contains *{items}*\!\n\n" \
                          f"http://withhive\.me/313/{promocode}"

        # in current implementation users data
        # stored in file "subbed_users" in json and looks like
        # {"user_id": "user_username(if exists, else None)", ...}
        for user_id in users.keys():
            await bot.send_message(user_id,
                                   message_to_send,
                                   # disable_notification=True,
                                   parse_mode=aiogram.types.ParseMode.MARKDOWN_V2,
                                   disable_web_page_preview=True)

    with open(path_to_file_with_previous_check, "w") as updated_previous:
        updated_previous.write(current_check_data)
