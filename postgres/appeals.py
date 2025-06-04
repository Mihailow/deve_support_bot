from postgres.postgres_queries import *
from config import telegram_token


# добавить обращение
async def insert_appeal(user_id, appeal_id, question_text, localization):
    await postgres_do_query("INSERT INTO appeals (token, appeal_id, user_id, question_text, localization, status) "
                            "VALUES (%s, %s, %s, %s, %s, %s);",
                            (telegram_token, appeal_id, user_id, question_text, localization, "Создано",))
    return await postgres_select_one("SELECT * FROM appeals WHERE token = %s AND user_id = %s ORDER BY id DESC LIMIT 1",
                                     (telegram_token, user_id,))


# добавить категорию в обращение
async def update_appeal_category_user(category_id, appeal_id):
    await postgres_do_query("UPDATE appeals SET category_id = %s, date_create = NOW() WHERE id = %s;",
                            (category_id, appeal_id,))


# изменить категорию обращения
async def update_appeal_category_admin(appeal_id, category_id, ):
    await postgres_do_query("UPDATE appeals SET category_id = %s WHERE token = %s AND id = %s",
                            (category_id, telegram_token, appeal_id,))


# добавить админа в обращение
async def update_appeal_admin(manager_id, appeal_id, status, add=True):
    if add:
        await postgres_do_query("UPDATE appeals SET manager_id = %s, status = %s, date_get_in_work = NOW() WHERE token = %s AND id = %s",
                                (manager_id, status, telegram_token, appeal_id,))
    else:
        await postgres_do_query("UPDATE appeals SET manager_id = null, status = %s, date_get_in_work = null WHERE token = %s AND id = %s",
                                (status, telegram_token, appeal_id,))


# изменить статус обращения
async def update_appeal_status(appeal_id, status):
    await postgres_do_query("UPDATE appeals SET status = %s WHERE token = %s AND id = %s",
                            (status, telegram_token, appeal_id,))


# получить последнее обращение пользователя
async def get_last_unfinished_user_appeal(user_id):
    return await postgres_select_one("SELECT * FROM appeals WHERE token = %s AND user_id = %s AND date_create IS NOT NULL ORDER BY id DESC LIMIT 1",
                                     (telegram_token, user_id,))


# получить обращение по id
async def get_appeal(appeal_id):
    return await postgres_select_one("SELECT * FROM appeals WHERE token = %s AND id = %s",
                                     (telegram_token, appeal_id,))


# получить обращение по appeal_id
async def get_appeal_with_id(appeal_id):
    return await postgres_select_one("SELECT * FROM appeals WHERE token = %s AND appeal_id = %s",
                                     (telegram_token, appeal_id,))


# получить количество незаконченных обращений
async def get_user_appeals_count(user_id):
    count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND user_id = %s AND status != %s",
                                      (telegram_token, user_id, "Завершено",))
    return count["count"]


# получить все обращения которые без категории и более суток
async def get_new_old_appeals():
    return await postgres_select_all("SELECT * FROM appeals WHERE token = %s AND NOW()-date_create > interval '1 day'",
                                     (telegram_token,))


# получить все обращения которые без работы
async def get_new_appeals_without_work():
    return await postgres_select_all("SELECT * FROM appeals WHERE token = %s AND status = %s AND date_create IS NOT NULL",
                                     (telegram_token, "Создано"))


# получить все обращения которые в работе
async def get_appeals_in_work():
    return await postgres_select_all("SELECT * FROM appeals WHERE token = %s AND status = %s",
                                     (telegram_token, "В работе"))


# удалить обращение
async def del_appeal(appeal_id):
    await postgres_do_query("DELETE FROM appeals WHERE token = %s and id = %s",
                            (telegram_token, appeal_id,))


# получить количество активных обращений пользователя
async def get_admin_appeals_count(manager_id):
    count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND manager_id = %s AND status = %s",
                                      (telegram_token, manager_id, "В работе",))
    return count["count"]


# получить количество завершенных обращений у менеджера
async def get_admin_finished_appeals_count(manager_id, days):
    count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND status = %s AND NOW()-"
                                      "(SELECT date_send FROM appeal_history WHERE appeal_history.appeal_id = appeals.id ORDER BY id DESC LIMIT 1) < interval %s",
                                      (telegram_token, "Завершено", days,))
    return count["count"]


# получить до 10 обращений в зависимости от страницы
async def get_appeals_on_page(appeals_page, manager_id, status, admin):
    offset = int(str(appeals_page) + "0") - 10
    if admin:
        return await postgres_select_all(
            "SELECT * FROM appeals WHERE token = %s AND status = %s LIMIT 10 OFFSET %s",
            (telegram_token, status, offset,))
    if status != "Создано":
        return await postgres_select_all(
            "SELECT * FROM appeals WHERE token = %s AND manager_id = %s AND status = %s LIMIT 10 OFFSET %s",
            (telegram_token, manager_id, status, offset,))
    else:
        return await postgres_select_all(
            "SELECT appeals.id, appeals.appeal_id, appeals.user_id, appeals.manager_id, appeals.category_id, appeals.question_text "
            "FROM appeals, managers WHERE appeals.token = %s AND appeals.status = %s "
            "AND get_category_main_father(%s, appeals.category_id) = managers.category_id "
            "AND managers.manager_id = %s LIMIT 10 OFFSET %s",
            (telegram_token, status, telegram_token, manager_id, offset,))


# получить количество страниц обращений
async def get_appeals_page_count(manager_id, status, admin):
    if admin:
        count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND status = %s",
                                          (telegram_token, status,))
    elif status != "Создано":
        count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND manager_id = %s AND status = %s",
                                          (telegram_token, manager_id, status,))
    else:
        count = await postgres_select_one("SELECT COUNT(*) FROM appeals, managers WHERE appeals.token = %s AND appeals.status = %s "
                                          "AND get_category_main_father(%s, appeals.category_id) = managers.category_id AND managers.manager_id = %s",
                                          (telegram_token, status, telegram_token, manager_id,))
    if count["count"] == 0:
        return 1
    if count["count"] % 10 == 0:
        return count["count"] // 10
    return count["count"] // 10 + 1


# получить до 10 обращений в зависимости от страницы
async def get_user_appeals_on_page(appeals_page, user_id, status):
    offset = int(str(appeals_page) + "0") - 10
    a = await postgres_select_all(
            "SELECT * FROM appeals WHERE token = %s AND user_id = %s AND status = %s LIMIT 10 OFFSET %s",
            (telegram_token, user_id, status, offset,))
    return a


# получить количество страниц обращений
async def get_user_appeals_page_count(user_id, status):
    count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND user_id = %s AND status = %s",
                                      (telegram_token, user_id, status,))
    if count["count"] == 0:
        return 1
    if count["count"] % 10 == 0:
        return count["count"] // 10
    return count["count"] // 10 + 1


# получить количество завершенных обращений у менеджера
async def get_appeals_count_interval(days):
    count = await postgres_select_one("SELECT COUNT(*) FROM appeals WHERE token = %s AND NOW()-"
                                      "(SELECT date_send FROM appeal_history WHERE appeal_history.appeal_id = appeals.id ORDER BY id DESC LIMIT 1) < interval %s",
                                      (telegram_token, days,))
    return count["count"]

