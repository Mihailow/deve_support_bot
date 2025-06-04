from postgres.postgres_queries import *
from config import telegram_token


# добавить нового
async def insert_user(nickname, first_name, last_name, user_id, localization):
    if await postgres_select_one("SELECT user_id FROM users WHERE token = %s AND user_id = %s",
                                 (telegram_token, user_id,)) is None:
        await postgres_do_query("INSERT INTO users (token, nickname, first_name, last_name, user_id, "
                                "date_registration, blocked, localization) "
                                "VALUES (%s, %s, %s, %s, %s, NOW(), false, %s)",
                                (telegram_token, nickname, first_name, last_name, user_id, localization,))
    else:
        await update_user(nickname, first_name, last_name, user_id)


# обновить данные
async def update_user(nickname, first_name, last_name, user_id):
    await postgres_do_query("UPDATE users SET nickname = %s, first_name = %s, last_name = %s "
                            "WHERE token = %s AND user_id = %s",
                            (nickname, first_name, last_name, telegram_token, user_id,))


# обновить локализацию
async def update_user_localization(user_id, localization):
    await postgres_do_query("UPDATE users SET localization = %s WHERE token = %s AND user_id = %s",
                            (localization, telegram_token, user_id,))


# обновить локализацию
async def update_user_blocked(user_id):
    await postgres_do_query("UPDATE users SET blocked = NOT (SELECT blocked FROM users "
                            "WHERE token = %s AND user_id = %s) "
                            "WHERE token = %s AND user_id = %s",
                            (telegram_token, user_id, telegram_token, user_id,))


# получить всё
async def get_user_info(user_id):
    return await postgres_select_one("SELECT * FROM users WHERE token = %s AND user_id = %s",
                                     (telegram_token, user_id,))


# получить локализацию
async def get_user_localization(user_id):
    localization = await postgres_select_one("SELECT localization FROM users WHERE token = %s AND user_id = %s",
                                             (telegram_token, user_id))
    return localization['localization']


async def get_user_by_username(username):
    return await postgres_select_one("SELECT * FROM users WHERE token = %s AND nickname = %s",
                                     (telegram_token, username))


async def get_user_is_blocked(user_id):
    user = await postgres_select_one("SELECT * FROM users WHERE token = %s AND user_id = %s",
                                     (telegram_token, user_id))
    if user:
        return user["blocked"]
    return False
