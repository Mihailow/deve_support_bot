from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from postgres.settings import get_setting
from postgres.users import get_user_localization
from translations import _, translations


# Главная клавиатура
## Бот создан на платформе DeveBot
## Часто задаваемые вопросы
## Задать свой вопрос
async def main_keyboard(user_id):
    keyboard = ReplyKeyboardMarkup()
    if await get_setting("advertisement"):
        keyboard.add(KeyboardButton(text="🤖 " + await _("Бот создан на платформе", await get_user_localization(user_id)) + " DeveBot 🤖"))
    keyboard.add(KeyboardButton(text=await _("❔ Часто задаваемые вопросы ❔", await get_user_localization(user_id))))
    keyboard.add(KeyboardButton(text=await _("Задать свой вопрос", await get_user_localization(user_id))))
    return keyboard


# Закрыть сообщение
## отмена
async def close_keyboard(user_id):
    keyboard = (InlineKeyboardMarkup(row_width=1))
    keyboard.add(InlineKeyboardButton(text=await _("Отмена", await get_user_localization(user_id)), callback_data="close"))
    return keyboard


## доступные языки
async def language_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for language in translations:
        keyboard.add(InlineKeyboardButton(text=language, callback_data=f"set_user_language_{language}"))
    return keyboard
