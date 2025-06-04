from datetime import datetime, timedelta
from random import randint
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from translations import _
from config import telegram_token

from keyboards.admin_keyboards import *
from keyboards.manager_keyboarads import *
from keyboards.user_keyboarads import *
from keyboards.all_keyboarads import *

from postgres.appeal_history import *
from postgres.appeal_notices import *
from postgres.appeals import *
from postgres.categories import *
from postgres.from_website import *
from postgres.mailings import *
from postgres.managers import *
from postgres.new_messages import *
from postgres.settings import *
from postgres.shown_appeals import *
from postgres.users import *

from mailingsSystems import AlbumMiddleware

bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AlbumMiddleware())
scheduler = AsyncIOScheduler()

user_category_page = {}
user_appeal_page = {}
user_in_category = {}
user_answer_to = {}
user_category_father = {}


class Status(StatesGroup):
    create_appeal = State()
    choose_category = State()
    change_category = State()
    answer = State()
    find_user = State()

    change_media_state = State()
    new_mailing_state = State()
    add_text_state = State()
    change_text_state = State()


# генерация id обращения
async def generate_appeal_id():
    while True:
        appeal_id = randint(10 ** 8, 10 ** 9)
        if await get_appeal_with_id(appeal_id) is None:
            return appeal_id


# отправить уведомление менеджерам
async def send_to_admins(managers_id, appeal_id, appeal_show_id, category_name, question_text, user_name, miss_manager_id=0):
    for manager_id in managers_id:
        if manager_id["manager_id"] != miss_manager_id:
            msg = await bot.send_message(manager_id["manager_id"], text=f"{await _('Обращение', await get_user_localization(manager_id['manager_id']))}: #{appeal_show_id}\n"
                                                                        f"{await _('Категория', await get_user_localization(manager_id['manager_id']))}: {await _(category_name, await get_user_localization(manager_id['manager_id']))}\n"
                                                                        f"{await _('Сообщение', await get_user_localization(manager_id['manager_id']))}: {question_text}\n"
                                                                        f"{await _('Пользователь', await get_user_localization(manager_id['manager_id']))}: @{user_name}",
                                         reply_markup=await manager_new_appeal_notice_keyboard(appeal_id, manager_id['manager_id']))
            await insert_appeal_notice(appeal_id, manager_id["manager_id"], msg.message_id, True)


# удалять обращения, которые висят более суток
async def del_new_appeals_without_category():
    appeals = await get_new_old_appeals()
    for appeal in appeals:
        await del_appeal(appeal["id"])


# переотправить обращения которые 30 мин не берут в работу
async def resend_new_appeals():
    appeals = await get_new_appeals_without_work()
    for appeal in appeals:
        notices = await get_appeal_notices_managers(appeal["id"])
        await del_appeal_notices_managers(appeal["id"])
        for notice in notices:
            await bot.delete_message(notice["user_id"], notice["message_id"])
        user = await get_user_info(appeal["user_id"])
        category_id = await get_category_main_father(appeal["category_id"])
        await send_to_admins(await get_managers_id(category_id), appeal["id"], appeal["appeal_id"],
                             await get_category_name(appeal["category_id"]), appeal["question_text"],
                             user["nickname"])


# отправить напоминание о незакрытом обращении
async def notice_old_appeals():
    appeals = await get_appeals_in_work()
    for appeal in appeals:
        last_mess = await get_last_message(appeal["id"])
        if appeal["manager_id"]:
            interval = datetime.now() - last_mess["date_send"]
            if interval > timedelta(minutes=30):
                notice = await get_appeal_notices_managers(appeal["id"])
                await bot.send_message(appeal["manager_id"], f"{await _('По обращению', await get_user_localization(appeal['manager_id']))} "
                                                             f"№{appeal['appeal_id']} "
                                                             f"{await _('давно не было активности', await get_user_localization(appeal['manager_id']))}",
                                       reply_to_message_id=notice[0]["message_id"])


async def send_admin_text(user_id, owner_id, manager):
    if user_id == owner_id:
        bot_info = await bot.get_me()
        admin = await get_user_info(user_id)

        answer_text = await _("ℹ️ Информация:", await get_user_localization(user_id)) + "\n\n"
        answer_text += await _("├Бот:", await get_user_localization(user_id)) + " " + bot_info.first_name + "\n"
        answer_text += await _("├Ник:", await get_user_localization(user_id)) + " " + bot_info.username + "\n"
        answer_text += await _("├Статус:", await get_user_localization(user_id)) + " " + await get_setting("status") + "\n"
        answer_text += await _("├Создатель:", await get_user_localization(user_id)) + " @" + admin["nickname"] + "\n"
        answer_text += await _("└Создан:", await get_user_localization(user_id)) + " " + str(await get_setting("date_created")) + "\n\n"
        answer_text += await _("🌐 Сервер:", await get_user_localization(user_id)) + "\n"
        answer_text += await _("├Тариф:", await get_user_localization(user_id)) + " " + await get_setting("rate") + "\n"
        # answer_text += await _("└Оплата до:", await get_user_localization(user_id)) + " " + "---" + "\n\n"
        answer_text += await _("🙍 Информация об обращениях:", await get_user_localization(user_id)) + "\n"
        answer_text += await _("├ За месяц:", await get_user_localization(user_id)) + " " + str(await get_appeals_count_interval("1 month")) + "\n"
        answer_text += await _("├ За неделю:", await get_user_localization(user_id)) + " " + str(await get_appeals_count_interval("7 day")) + "\n"
        answer_text += await _("└ За день:", await get_user_localization(user_id)) + " " + str(await get_appeals_count_interval("1 day")) + "\n"
        await bot.send_message(user_id, answer_text, reply_markup=await admin_keyboard(user_id, True))

    elif manager:
        categories = await get_manager_categories(user_id)

        answer_text = await _("ℹ️ Информация:", await get_user_localization(user_id)) + "\n\n"
        if len(categories) == 1:
            answer_text += {await _("Вы работаете с ", await get_user_localization(user_id))}
            answer_text += await _(await get_category_name(categories[0]["category_id"]), await get_user_localization(user_id))
        else:
            answer_text += await _("Категории с которыми вы работаете:", await get_user_localization(user_id)) + "\n"
            for i in range(len(categories)):
                answer_text += f"{i + 1}) {await _(await get_category_name(categories[i]['category_id']), await get_user_localization(user_id))}\n"
        answer_text += (
            f"\n{await _('🙍 Информация о ваших обращениях:', await get_user_localization(user_id))}\n\n"
            f"{await _('Активных: ', await get_user_localization(user_id))}{await get_admin_appeals_count(user_id)}\n"
            f"{await _('Закрыто:', await get_user_localization(user_id))}\n"
            f"{await _('├За месяц:', await get_user_localization(user_id))} {await get_admin_finished_appeals_count(user_id, '1 month')}\n"
            f"{await _('├За неделю:', await get_user_localization(user_id))} {await get_admin_finished_appeals_count(user_id, '7 day')}\n"
            f"{await _('└За день:', await get_user_localization(user_id))} {await get_admin_finished_appeals_count(user_id, '1 day')}\n")
        await bot.send_message(user_id, answer_text, reply_markup=await admin_keyboard(user_id, False))


# отправить напоминание о незакрытом обращении
async def send_message_to_user():
    new_messages = await get_new_messages()
    for new_message in new_messages:
        appeal = await get_appeal(new_message["appeal_id"])
        mes = await bot.send_message(appeal["user_id"], new_message["text"], reply_markup=await new_message_keyboard(appeal["id"], appeal["user_id"]))
        await insert_message(appeal["manager_id"], appeal["id"], mes.text, True)


# отправить напоминание о незакрытом обращении
async def change_settings_from_website():
    from_website = await get_from_website()
    for line in from_website:
        if line["type"] == "поменять менеджера":
            notices = await get_appeal_notices_managers(line["appeal_id"])
            await del_appeal_notices_managers(line["appeal_id"])
            for notice in notices:
                await bot.delete_message(notice["user_id"], notice["message_id"])
            appeal = await get_appeal(line["appeal_id"])
            await update_appeal_admin(None, line["appeal_id"], "Создано")
            user = await get_user_info(appeal["user_id"])
            category_id = await get_category_main_father(appeal["category_id"])
            await send_to_admins(await get_managers_id(category_id), appeal["id"], appeal["appeal_id"],
                                 await get_category_name(appeal["category_id"]),
                                 appeal["question_text"], user["nickname"], appeal["manager_id"])
        elif line["type"] == "изменить категорию":
            await update_appeal_category_admin(line["appeal_id"], line["category_id"])
            notices = await get_appeal_notices_managers(line["appeal_id"])
            await del_appeal_notices_managers(line["appeal_id"])
            for notice in notices:
                await bot.delete_message(notice["user_id"], notice["message_id"])
            appeal = await get_appeal(line["appeal_id"])
            admin = await get_user_info(appeal['manager_id'])
            user = await get_user_info(appeal["user_id"])
            msg = await bot.send_message(
                chat_id=appeal['manager_id'],
                text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
                     f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
                     f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
                     f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
                reply_markup=await manager_appeal_in_work_close_keyboard(appeal["id"], appeal['manager_id'],
                                                                         user["blocked"]))
            await insert_appeal_notice(appeal["id"], appeal['manager_id'], msg.message_id, True)
        elif line["type"] == "предложить закрыть":
            notices = await get_appeal_notices_managers(line["appeal_id"])
            await del_appeal_notices_managers(line["appeal_id"])
            for notice in notices:
                await bot.delete_message(notice["user_id"], notice["message_id"])
            appeal = await get_appeal(line["appeal_id"])
            admin = await get_user_info(appeal['manager_id'])
            user = await get_user_info(appeal["user_id"])
            msg = await bot.send_message(
                chat_id=appeal['manager_id'],
                text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
                     f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
                     f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
                     f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
                reply_markup=await manager_appeal_in_work_close_keyboard(appeal["id"], appeal['manager_id'],
                                                                         user["blocked"]))
            await insert_appeal_notice(appeal["id"], appeal['manager_id'], msg.message_id, True)
            msg = await bot.send_message(user["user_id"], await _("Ваш вопрос решён?",
                                                                  user['localization']),
                                         reply_markup=await new_message_keyboard(appeal["id"],
                                                                                 user['user_id']))
            await insert_appeal_notice(appeal["id"], user['user_id'], msg.message_id, False)
