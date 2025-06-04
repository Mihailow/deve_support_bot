from postgres.postgres_queries import *
from config import telegram_token


# создать предварительное сообщение
async def insert_pre_message(user_id, appeal_id, message_text):
    await postgres_do_query("INSERT INTO appeal_history (token, appeal_id, message_text, user_id, is_manager) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (telegram_token, appeal_id, message_text, user_id, False,))


# добавить сообщение
async def insert_message(user_id, appeal_id, message_text, is_manager):
    await postgres_do_query("INSERT INTO appeal_history (token, appeal_id, date_send, message_text, user_id, is_manager) "
                            "VALUES (%s, %s, NOW(), %s, %s, %s)",
                            (telegram_token, appeal_id, message_text, user_id, is_manager))


# закрепить сообщение
async def update_pre_message(appeal_id,):
    await postgres_do_query("UPDATE appeal_history SET date_send = NOW() WHERE token = %s AND appeal_id = %s",
                            (telegram_token, appeal_id))


# получить последнее сообщение по обращению
async def get_last_message(appeal_id):
    return await postgres_select_one("SELECT * FROM appeal_history WHERE token = %s AND appeal_id = %s ORDER BY id DESC LIMIT 1",
                                     (telegram_token, appeal_id,))
