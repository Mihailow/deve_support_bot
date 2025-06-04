from postgres.postgres_queries import *
from config import telegram_token


# добавить менеджера
async def insert_manager(user_id, category_id):
    await postgres_do_query("INSERT INTO managers (token, manager_id, category_id) "
                            "VALUES (%s, %s, %s)",
                            (telegram_token, user_id, category_id,))


# получить id менеджеров из категории
async def get_managers_id(category_id):
    return await postgres_select_all("SELECT manager_id FROM managers WHERE token = %s AND category_id = %s",
                                     (telegram_token, category_id,))


# получить менеджера
async def get_manager(manager_id):
    return await postgres_select_all("SELECT * FROM managers WHERE token = %s AND manager_id = %s",
                                     (telegram_token, manager_id,))


# получить категории менеджера
async def get_manager_categories(manager_id):
    return await postgres_select_all("SELECT DISTINCT category_id FROM managers WHERE token = %s AND manager_id = %s",
                                     (telegram_token, manager_id,))
