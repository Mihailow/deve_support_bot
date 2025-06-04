from postgres.postgres_queries import *
from config import telegram_token


# получить конкретную настройку
async def get_setting(column):
    settings = await postgres_select_one("SELECT * FROM settings WHERE token = %s",
                                         (telegram_token,))
    return settings[column]


# проверить на админа
async def get_is_admin(user_id):
    settings = await postgres_select_one("SELECT * FROM settings WHERE token = %s",
                                         (telegram_token,))
    if settings["owner_id"] == user_id:
        return True
    else:
        return False