from aiogram import types

keyboard = types.InlineKeyboardMarkup()
promo_button = types.InlineKeyboardButton(text='Get promocodes!', callback_data="promo")
keyboard.add(promo_button)
keyboard_without_buttons = types.InlineKeyboardMarkup()
