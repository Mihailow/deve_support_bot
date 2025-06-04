from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from postgres.settings import get_setting
from postgres.users import get_user_localization
from translations import _


async def show_categories_appeals_keyboard(categories_on_page, shown_appeals_on_page, user_category_page, page_count, user_id):
    if page_count == 0:
        user_category_page = 0
    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in categories_on_page:
        keyboard.add(InlineKeyboardButton(text=await _(category["category_name"], await get_user_localization(user_id)), callback_data=f"show_category_number_{category['id']}"))
    for appeal in shown_appeals_on_page:
        keyboard.add(InlineKeyboardButton(text=await _(appeal["question_text"], await get_user_localization(user_id)), callback_data=f"shown_appeal_number_{appeal['id']}"))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data="show_category_back"),
                 InlineKeyboardButton(text=f"{user_category_page}/{page_count}", callback_data="nothing"),
                 InlineKeyboardButton(text="▶️", callback_data="show_category_next"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_show_categories"))
    return keyboard


# Категории при создании обращения
## список категорий
## назад; номер страницы/все страницы; вперёд
async def show_categories_for_create_question_keyboard(categories_on_page, user_category_page, categories_page_count, appeal_id, user_id):
    if categories_page_count == 0:
        user_category_page = 0
    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in categories_on_page:
        keyboard.add(InlineKeyboardButton(text=await _(category["category_name"], await get_user_localization(user_id)), callback_data=f"show_category_number_{category['id']}_{appeal_id}"),
                     InlineKeyboardButton(text=await _("Выбрать", await get_user_localization(user_id)), callback_data=f"set_category_number_{category['id']}_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"show_category_back_{appeal_id}"),
                 InlineKeyboardButton(text=f"{user_category_page}/{categories_page_count}", callback_data="nothing"),
                 InlineKeyboardButton(text="▶️", callback_data=f"show_category_next_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_show_categories_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Отправить без категории", await get_user_localization(user_id)), callback_data=f"set_category_number_0_{appeal_id}"))
    return keyboard


# Просмотр избранного обращения
## Назад к вопросам
## Не понятно? Напишите в поддержку
async def look_shown_appeal_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_show_categories_from_appeal"))
    if await get_setting("text_under_shown_appeal_to_create"):
        keyboard.add(InlineKeyboardButton(text=await _("Не понятно? Напишите в поддержку", await get_user_localization(user_id)), callback_data="create_appeal"))
    return keyboard


# Новое сообщение пользователю
## написать ответ
## закрыть обращение
async def new_message_keyboard(appeal_id, user_id):
    keyboard = (InlineKeyboardMarkup(row_width=2))
    keyboard.add(InlineKeyboardButton(text=await _("Написать ответ", await get_user_localization(user_id)), callback_data=f"answer_{appeal_id}",),
                 InlineKeyboardButton(text=await _("Закрыть обращение", await get_user_localization(user_id)), callback_data=f"close_{appeal_id}"))
    return keyboard
