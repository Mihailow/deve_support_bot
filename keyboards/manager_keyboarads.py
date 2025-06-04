from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from postgres.users import get_user_localization
from translations import _


# Просмотр обращения в /admin/status
## Посмотреть переписку
## Назад
async def managers_appeals_back_keyboard(user_id, status):
    keyboard = (InlineKeyboardMarkup(row_width=1))
    keyboard.add(InlineKeyboardButton(text=await _("Посмотреть переписку", await get_user_localization(user_id)), url="https://ya.ru/"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_managers_appears_{status}"))
    return keyboard


# Просмотр списка обращений менеджера
## список обращений
## назад; номер страницы/все страницы; вперёд
## назад
async def managers_appeals_keyboard(appeals_on_page, user_appeal_page, appeals_page_count, status, user_id):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for appeal in appeals_on_page:
        keyboard.add(InlineKeyboardButton(text=appeal["appeal_id"], callback_data=f"manager_appeal_number_{appeal['id']}_{status}"))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"manager_appeal_back_{status}"),
                 InlineKeyboardButton(text=f"{user_appeal_page}/{appeals_page_count}", callback_data="nothing"),
                 InlineKeyboardButton(text="▶️", callback_data=f"manager_appeal_next_{status}"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data="back_to_admin"))
    return keyboard


# Новое обращение
## Взять в работу
## Изменить категорию
async def manager_new_appeal_notice_keyboard(appeal_id, user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text=await _("Взять в работу", await get_user_localization(user_id)), callback_data=f"take_in_work_{appeal_id}"),
                 InlineKeyboardButton(text=await _("Изменить категорию", await get_user_localization(user_id)), callback_data=f"change_appeal_category_{appeal_id}"))
    return keyboard


# Обращение в работе
## Предложить закрыть обращение; Изменить менеджера
## Перейти к работе
async def manager_appeal_in_work_keyboard(appeal_id, user_id, blocked):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text=await _("Предложить закрыть обращение", await get_user_localization(user_id)), callback_data=f"suggest_closing_{appeal_id}"),
                 InlineKeyboardButton(text=await _("Изменить менеджера", await get_user_localization(user_id)), callback_data=f"change_appeal_manager_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Перейти к работе", await get_user_localization(user_id)), url="https://ya.ru/"))
    if blocked:
        keyboard.add(InlineKeyboardButton(text=await _("Разблокировать", await get_user_localization(user_id)), callback_data=f"block_user_owner_{appeal_id}"))
    else:
        keyboard.add(InlineKeyboardButton(text=await _("Заблокировать", await get_user_localization(user_id)), callback_data=f"block_user_owner_{appeal_id}"))
    return keyboard


# Обращение в работе, после предложения закрыть
## закрыть обращение; Изменить менеджера
## Перейти к работе
async def manager_appeal_in_work_close_keyboard(appeal_id, user_id, blocked):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text=await _("Закрыть обращение", await get_user_localization(user_id)), callback_data=f"close_{appeal_id}"),
                 InlineKeyboardButton(text=await _("Изменить менеджера", await get_user_localization(user_id)), callback_data=f"change_appeal_manager_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Перейти к работе", await get_user_localization(user_id)), url="https://ya.ru/"))
    if blocked:
        keyboard.add(InlineKeyboardButton(text=await _("Разблокировать", await get_user_localization(user_id)),
                                          callback_data=f"block_user_owner_{appeal_id}"))
    else:
        keyboard.add(InlineKeyboardButton(text=await _("Заблокировать", await get_user_localization(user_id)),
                                          callback_data=f"block_user_owner_{appeal_id}"))
    return keyboard


# Категории при создании обращения
## список категорий
## назад; номер страницы/все страницы; вперёд
async def manager_change_category_keyboard(categories_on_page, user_category_page, categories_page_count, appeal_id, user_id):
    if categories_page_count == 0:
        user_category_page = 0
    keyboard = InlineKeyboardMarkup(row_width=3)
    for category in categories_on_page:
        keyboard.add(InlineKeyboardButton(text=await _(category["category_name"], await get_user_localization(user_id)), callback_data=f"show_change_category_number_{category['id']}_{appeal_id}"),
                     InlineKeyboardButton(text=await _("Выбрать", await get_user_localization(user_id)), callback_data=f"change_category_number_{category['id']}_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"change_category_back_{appeal_id}"),
                 InlineKeyboardButton(text=f"{user_category_page}/{categories_page_count}", callback_data="nothing"),
                 InlineKeyboardButton(text="▶️", callback_data=f"change_category_next_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Новые вопросы", await get_user_localization(user_id)), callback_data=f"change_category_number_0_{appeal_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_show_categories_{appeal_id}"))
    return keyboard
