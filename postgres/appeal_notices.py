from postgres.postgres_queries import *
from config import telegram_token


# добавить уведомление
async def insert_appeal_notice(appeal_id, user_id, message_id, is_manager):
    await postgres_do_query("INSERT INTO appeal_notices (token, appeal_id, message_id, user_id, is_manager) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (telegram_token, appeal_id, message_id, user_id, is_manager,))


# получить все уведомления по обращению у менеджеров
async def get_appeal_notices_managers(appeal_id):
    return await postgres_select_all("SELECT * FROM appeal_notices WHERE token = %s AND appeal_id = %s AND is_manager = true",
                                     (telegram_token, appeal_id,))


# удалить все уведомления у менеджеров
async def del_appeal_notices_managers(appeal_id):
    await postgres_do_query("DELETE FROM appeal_notices WHERE token = %s AND appeal_id = %s AND is_manager = true",
                            (telegram_token, appeal_id,))
