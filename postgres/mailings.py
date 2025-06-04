from postgres.postgres_queries import *
from config import telegram_token


async def get_mailling_from_db(mailing_id):
    return await postgres_select_one(f"SELECT * from mailings where mailing_id = %s AND token = %s;",
                                     (mailing_id, telegram_token))


async def update_mailling_in_db(text, name_mailing, id_mailing):
    await postgres_do_query(
        "UPDATE mailings SET mailing_text = %s, mailing_name = %s WHERE mailing_id = %s AND token = %s;",
        (text, name_mailing, id_mailing, telegram_token))


async def get_all_mailling_from_db():
    return await postgres_select_all(f"SELECT mailing_name, mailing_id FROM mailings WHERE token = %s;",
                                     (telegram_token,))


async def get_all_userid_from_db():
    return await postgres_select_all(f"SELECT user_id FROM users WHERE token = %s;",
                                     (telegram_token,))


async def set_mailing_media_array_in_db(info):
    await postgres_do_query(
        "UPDATE mailings SET mailing_media_array = %s WHERE mailing_id = %s AND token = %s",
        (info['media'], info['id_mailing'], telegram_token))


async def update_mailling_users_count_in_db(is_except):
    if is_except:
        await postgres_do_query(
            "UPDATE mailings SET mailing_error_sent = mailing_error_sent + 1, "
            "mailing_total_sent = mailing_total_sent + 1 WHERE token = %s;", (telegram_token,))
    else:
        await postgres_do_query(
            "UPDATE mailings SET mailing_ok_sent = mailing_ok_sent + 1, "
            "mailing_total_sent = mailing_total_sent + 1 WHERE token = %s;", (telegram_token,))


async def add_mailing_complete_in_db():
    await postgres_do_query(
        "UPDATE mailings SET mailing_complete = mailing_complete + 1 WHERE token = %s;",
        (telegram_token,))


async def delete_mailling_from_db(id_mailing):
    await postgres_do_query(
        "DELETE FROM mailings WHERE mailing_id = %s AND token = %s",
        (id_mailing, telegram_token,))
