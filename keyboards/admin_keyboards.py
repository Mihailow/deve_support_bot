from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from postgres.users import get_user_localization
from translations import _


# админ/менеджер
## Оплатить/повысить тариф
## Настройки бота
## Управление пользователями
## Управление рассылками
## Активные обращения
## Новые обращения
## Закрытые обращения
## Закрыть
async def admin_keyboard(user_id, admin):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if admin:
        keyboard.add(InlineKeyboardButton(text=await _("Оплатить/повысить тариф", await get_user_localization(user_id)), url="https://ya.ru/"))
        keyboard.add(InlineKeyboardButton(text=await _("Настройки бота", await get_user_localization(user_id)), url="https://ya.ru/"))
        keyboard.add(InlineKeyboardButton(text=await _("Управление пользователями", await get_user_localization(user_id)), callback_data="user_settings"))
        keyboard.add(InlineKeyboardButton(text=await _("Управление рассылками", await get_user_localization(user_id)), callback_data="mailing_settings"))
    keyboard.add(InlineKeyboardButton(text=await _("Активные обращения", await get_user_localization(user_id)), callback_data="show_active_appeals"))
    keyboard.add(InlineKeyboardButton(text=await _("Новые обращения", await get_user_localization(user_id)), callback_data="show_new_appeals"))
    keyboard.add(InlineKeyboardButton(text=await _("Закрытые обращения", await get_user_localization(user_id)), callback_data="show_close_appeals"))
    keyboard.add(InlineKeyboardButton(text=await _("Закрыть", await get_user_localization(user_id)), callback_data="close"))
    return keyboard


# управление пользователями
## Поиск пользователя по USERNAME
## Назад
async def user_settings_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=await _("Поиск пользователя по USERNAME", await get_user_localization(user_id)), callback_data="find_user_by_id"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data="back_to_admin"))
    return keyboard


# управление рассылками
## Добавить рассылку
## Добавить рассылку и сразу запустить
## Назад
async def mailing_settings_keyboard(list_mailing_text, user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    # keyboard.add(InlineKeyboardButton(text=await _("Добавить рассылку", await get_user_localization(user_id)), callback_data="add_mailing"))
    keyboard.add(InlineKeyboardButton(text=await _("Сформировать и запустить рассылку", await get_user_localization(user_id)), callback_data="go_mailing"))
    for i in list_mailing_text:
        keyboard.add(InlineKeyboardButton(text=f"⚫ {i['mailing_name']}", callback_data=f"mailing@{i['mailing_id']}"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data="back_to_admin"))
    return keyboard


# Нашёлся пользователь
## Активные обращения
## Новые обращения
## Закрытые обращения
## Разблокировать/Заблокировать
## Назад
async def user_find_keyboard(blocked, find_user_id, user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text=await _("Активные обращения", await get_user_localization(user_id)), callback_data=f"user_active_appeals_{find_user_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Новые обращения", await get_user_localization(user_id)), callback_data=f"user_new_appeals_{find_user_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Закрытые обращения", await get_user_localization(user_id)), callback_data=f"user_close_appeals_{find_user_id}"))
    if blocked:
        keyboard.add(InlineKeyboardButton(text=await _("Разблокировать", await get_user_localization(user_id)), callback_data=f"block_user_{find_user_id}"))
    else:
        keyboard.add(InlineKeyboardButton(text=await _("Заблокировать", await get_user_localization(user_id)), callback_data=f"block_user_{find_user_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data="back_to_admin"))
    return keyboard


# Просмотр обращения от пользователя
## Посмотреть переписку
## Назад
async def user_appeals_back_keyboard(user_id, status, find_user_id):
    keyboard = (InlineKeyboardMarkup(row_width=1))
    keyboard.add(InlineKeyboardButton(text=await _("Посмотреть переписку", await get_user_localization(user_id)), url="https://ya.ru/"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_user_appears_{status}_{find_user_id}"))
    return keyboard


# Просмотр списка обращений пользователя
## список обращений
## назад; номер страницы/все страницы; вперёд
## назад
async def user_appeals_keyboard(appeals_on_page, user_appeal_page, appeals_page_count, status, find_user_id, user_id):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for appeal in appeals_on_page:
        keyboard.add(InlineKeyboardButton(text=appeal["appeal_id"], callback_data=f"user_appeal_number_{appeal['id']}_{status}"))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"user_appeal_back_{status}_{find_user_id}"),
                 InlineKeyboardButton(text=f"{user_appeal_page}/{appeals_page_count}", callback_data="nothing"),
                 InlineKeyboardButton(text="▶️", callback_data=f"user_appeal_next_{status}_{find_user_id}"))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data=f"back_to_user_find_{find_user_id}"))
    return keyboard


async def back_to_admin_keyboard(user_id):
    keyboard = (InlineKeyboardMarkup(row_width=1))
    keyboard.add(InlineKeyboardButton(text=await _("Назад", await get_user_localization(user_id)), callback_data="back_to_admin"))
    return keyboard


async def get_main_mailings_keyboards(user_id) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=await _('Изменить', await get_user_localization(user_id)),
                             callback_data='change_mailing'),
        InlineKeyboardButton(text=await _('Запустить', await get_user_localization(user_id)),
                             callback_data='run_mailing'),
        # types.InlineKeyboardButton(text="Запустить с задержкой", callback_data='delay_run_mailing'),
        InlineKeyboardButton(text=await _('Получить тестовое сообщение', await get_user_localization(user_id)),
                             callback_data='get_test_mailing'),
        InlineKeyboardButton(text=await _('Удалить', await get_user_localization(user_id)),
                             callback_data='delete_mailing'),
        InlineKeyboardButton(text=f"◀ {await _('Назад', await get_user_localization(user_id))}",
                             callback_data='mailing_button')
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
