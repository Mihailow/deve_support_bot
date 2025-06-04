from postgres.postgres_queries import *
from config import telegram_token


async def get_from_website():
    from_website = await postgres_select_all("SELECT * FROM from_website WHERE token = %s",
                                             (telegram_token,))
    await postgres_do_query("DELETE FROM from_website WHERE token = %s",
                            (telegram_token,))
    return from_website
