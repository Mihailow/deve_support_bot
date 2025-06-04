from postgres.postgres_queries import *
from config import telegram_token


# получить обращение
async def get_shown_appeals(appeal_id):
    return await postgres_select_one("SELECT * FROM shown_appeals WHERE token = %s AND id = %s",
                                     (telegram_token, appeal_id,))


# получить до 10 обращений в зависимости от страницы
async def get_shown_appeals_on_page(appeals_page, category_id):
    offset = int(str(appeals_page) + "0") - 10
    shown_appeals = await postgres_select_all(
        "SELECT * FROM shown_appeals WHERE token = %s AND category_id = %s LIMIT 10 OFFSET %s",
        (telegram_token, category_id, offset,))
    return shown_appeals


# получить количество страниц обращений
async def get_shown_appeals_page_count(category_id):
    count = await postgres_select_one("SELECT COUNT(*) FROM shown_appeals WHERE token = %s AND category_id = %s",
                                      (telegram_token, category_id,))
    if count["count"] % 10 == 0:
        return count["count"] // 10
    return count["count"] // 10 + 1
