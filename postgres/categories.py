from postgres.postgres_queries import *
from config import telegram_token


# получить до 10 категорий в зависимости от страницы
async def get_categories_on_page(category_page, father):
    offset = int(str(category_page) + "0") - 10
    categories = await postgres_select_all("SELECT * FROM categories WHERE token = %s AND father = %s LIMIT 10 OFFSET %s",
                                           (telegram_token, father, offset,))
    return categories


# получить количество страниц категорий
async def get_categories_page_count(father):
    count = await postgres_select_one("SELECT COUNT(*) FROM categories WHERE token = %s AND father = %s",
                                      (telegram_token, father,))
    if count["count"] % 10 == 0:
        return count["count"] // 10
    return count["count"] // 10 + 1


# получить название категории
async def get_category_name(category_id):
    if category_id == 0:
        return "Новые вопросы"
    else:
        category = await postgres_select_one("SELECT category_name FROM categories WHERE token = %s AND id = %s",
                                             (telegram_token, category_id,))
        return category["category_name"]


async def get_category_father(category_id):
    category = await postgres_select_one("SELECT father FROM categories WHERE token = %s AND id = %s",
                                         (telegram_token, category_id,))
    return category["father"]


async def get_category_main_father(category_id):
    if category_id == "0":
        return 0
    category = await postgres_select_one("SELECT get_category_main_father(%s, %s)",
                                         (telegram_token, category_id))
    return category["get_category_main_father"]
