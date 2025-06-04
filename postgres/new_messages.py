from postgres.postgres_queries import *
from config import telegram_token


async def get_new_messages():
    new_messages = await postgres_select_all("SELECT * FROM new_messages WHERE token = %s",
                                             (telegram_token,))
    await postgres_do_query("DELETE FROM new_messages WHERE token = %s",
                            (telegram_token,))
    return new_messages
