from misc import *
from translations import _


# вернуться к выбору категорий
@dp.callback_query_handler(text="close", state="*")
async def but_close(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# ничего
@dp.callback_query_handler(text="nothing", state="*")
async def but_nothing(callback_query: types.CallbackQuery):
    return


# закрыть обращение
@dp.callback_query_handler(text_startswith="close_", state="*")
async def but_close_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    appeal = await get_appeal(callback_query.data[6:])
    if appeal["status"] == "Завершено":
        await callback_query.message.answer(
            await _("Обращение закрыто", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    appeal = await get_appeal(callback_query.data[6:])
    await update_appeal_status(appeal["id"], "Завершено")
    await insert_message(appeal["manager_id"], appeal['id'], "Обращение закрыто", True)
    await bot.send_message(appeal["user_id"],
                           await _("Ваше обращение закрыто", await get_user_localization(appeal["user_id"])),
                           reply_markup=await main_keyboard(appeal["user_id"]))
    await bot.send_message(appeal["manager_id"],
                           f"{await _('Запрос', await get_user_localization(appeal['manager_id']))}"
                           f" №{appeal['appeal_id']} "
                           f"{await _('закрыт', await get_user_localization(appeal['manager_id']))}",
                           reply_markup=await main_keyboard(appeal['manager_id']))
    notices = await get_appeal_notices_managers(appeal["id"])
    await del_appeal_notices_managers(appeal["id"])
    for notice in notices:
        await bot.delete_message(notice["user_id"], notice["message_id"])


# поменять язык
@dp.callback_query_handler(text_startswith="set_user_language_", state="*")
async def but_set_user_language_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await update_user_localization(callback_query.from_user.id, callback_query.data[18:])
    await callback_query.message.answer(
        await _('Здравствуйте!', await get_user_localization(callback_query.from_user.id)),
        reply_markup=await main_keyboard(callback_query.from_user.id))


# удаляет сообщение с кнопками при любом состоянии
@dp.callback_query_handler(state="*")
async def but_all(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


# /start
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message, state: FSMContext):
    if await get_user_is_blocked(message.from_user.id):
        await bot.send_message(message.from_user.id, await _("Вы заблокированы", await get_user_localization(message.from_user.id)))
        return
    await state.finish()
    await insert_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.id, message.from_user.language_code)
    await message.answer(await _('Здравствуйте!', await get_user_localization(message.from_user.id)),
                         reply_markup=await main_keyboard(message.from_user.id))
    if message.from_user.id in user_category_page.keys():
        del(user_category_page[message.from_user.id])
    if message.from_user.id in user_category_father.keys():
        del(user_category_father[message.from_user.id])
    if message.from_user.id in user_appeal_page.keys():
        del(user_appeal_page[message.from_user.id])
    if message.from_user.id in user_in_category.keys():
        del(user_in_category[message.from_user.id])
    if message.from_user.id in user_answer_to.keys():
        del(user_answer_to[message.from_user.id])


# /language
@dp.message_handler(commands=["language"], state="*")
async def command_language(message: types.Message, state: FSMContext):
    if await get_user_is_blocked(message.from_user.id):
        await bot.send_message(message.from_user.id, await _("Вы заблокированы", await get_user_localization(message.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(message.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(message.from_user.id)))
        return
    await state.finish()
    await update_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.id)
    await message.answer(await _('Выберите язык', await get_user_localization(message.from_user.id)),
                         reply_markup=await language_keyboard())
    if message.from_user.id in user_category_page.keys():
        del(user_category_page[message.from_user.id])
    if message.from_user.id in user_category_father.keys():
        del(user_category_father[message.from_user.id])
    if message.from_user.id in user_appeal_page.keys():
        del(user_appeal_page[message.from_user.id])
    if message.from_user.id in user_in_category.keys():
        del(user_in_category[message.from_user.id])
    if message.from_user.id in user_answer_to.keys():
        del(user_answer_to[message.from_user.id])


# любое другое сообщение
@dp.message_handler(content_types=["any"], state="*")
async def message_default(message: types.Message, state: FSMContext):
    if await get_user_is_blocked(message.from_user.id):
        await bot.send_message(message.from_user.id, await _("Вы заблокированы", await get_user_localization(message.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(message.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(message.from_user.id)))
        return
    await update_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.id)
    # Задать свой вопрос
    if message.text == f"🤖 {await _('Бот создан на платформе', await get_user_localization(message.from_user.id))} DeveBot 🤖":
        await state.finish()
        if message.from_user.id in user_category_page.keys():
            del (user_category_page[message.from_user.id])
        if message.from_user.id in user_category_father.keys():
            del (user_category_father[message.from_user.id])
        if message.from_user.id in user_appeal_page.keys():
            del (user_appeal_page[message.from_user.id])
        if message.from_user.id in user_in_category.keys():
            del (user_in_category[message.from_user.id])
        if message.from_user.id in user_answer_to.keys():
            del (user_answer_to[message.from_user.id])
        await message.answer(
            text=f"{await _('Бот создан на платформе', await get_user_localization(message.from_user.id))} <a href='https://deve-bot.com/'>DeveBot</a>",
            reply_markup=await main_keyboard(message.from_user.id), parse_mode="HTML")
    # Задать свой вопрос
    elif message.text == await _("Задать свой вопрос", await get_user_localization(message.from_user.id)):
        await state.finish()
        if message.from_user.id in user_category_page.keys():
            del (user_category_page[message.from_user.id])
        if message.from_user.id in user_category_father.keys():
            del (user_category_father[message.from_user.id])
        if message.from_user.id in user_appeal_page.keys():
            del (user_appeal_page[message.from_user.id])
        if message.from_user.id in user_in_category.keys():
            del (user_in_category[message.from_user.id])
        if message.from_user.id in user_answer_to.keys():
            del (user_answer_to[message.from_user.id])
        user_category_page[message.from_user.id] = 1
        user_category_father[message.from_user.id] = 0
        time = await get_last_unfinished_user_appeal(message.from_user.id)
        if time:
            time = datetime.now() - time["date_create"]
            min_time_between_appeals = timedelta(seconds=await get_setting("min_time_between_appeals"))
            if time < min_time_between_appeals:
                time = min_time_between_appeals - time
                await message.answer(
                    f"{await _('Вы превысили лимит вопросов, подождите', await get_user_localization(message.from_user.id))}"
                    f" {time.seconds} {await _('секунд', await get_user_localization(message.from_user.id))}",
                    reply_markup=await main_keyboard(message.from_user.id))
                return
        if await get_user_appeals_count(message.from_user.id) >= await get_setting("max_count_appeals"):
            await message.answer(await _("Вы превысили лимит необработанных вопросов",
                                         await get_user_localization(message.from_user.id)),
                                 reply_markup=await main_keyboard(message.from_user.id))
        else:
            await state.set_state(Status.create_appeal)
            await message.answer(
                await _("Напишите интересующий вас вопрос", await get_user_localization(message.from_user.id)),
                reply_markup=await close_keyboard(message.from_user.id))
    # Выбор темы вопроса
    elif message.text == await _("❔ Часто задаваемые вопросы ❔", await get_user_localization(message.from_user.id)):
        await state.finish()
        if message.from_user.id in user_category_page.keys():
            del (user_category_page[message.from_user.id])
        if message.from_user.id in user_appeal_page.keys():
            del (user_appeal_page[message.from_user.id])
        if message.from_user.id in user_in_category.keys():
            del (user_in_category[message.from_user.id])
        if message.from_user.id in user_answer_to.keys():
            del (user_answer_to[message.from_user.id])
        user_category_page[message.from_user.id] = 1
        user_category_father[message.from_user.id] = 0
        categories = await get_categories_on_page(user_category_page[message.from_user.id],
                                                  user_category_father[message.from_user.id])
        categories_page_count = await get_categories_page_count(user_category_father[message.from_user.id])
        shown_appeals = []
        shown_appeals_page_count = await get_shown_appeals_page_count(user_category_father[message.from_user.id])
        if not categories:
            shown_appeals = await get_shown_appeals_on_page(user_category_page[message.from_user.id] - categories_page_count,
                                                            user_category_father[message.from_user.id])
        await message.answer(await _("Выберите категорию", await get_user_localization(message.from_user.id)),
                             reply_markup=await show_categories_appeals_keyboard(
                                 categories, shown_appeals, user_category_page[message.from_user.id],
                                 categories_page_count + shown_appeals_page_count,
                                 message.from_user.id))
    elif await state.get_state() == "Status:create_appeal":
        await state.finish()
        await state.set_state(Status.choose_category)
        user = await get_user_info(message.from_user.id)
        appeal = await insert_appeal(user["user_id"], await generate_appeal_id(), message.text,
                                     user["localization"])
        await insert_pre_message(user["user_id"], appeal['id'], message.text)
        await message.answer(await _('Выберите категорию', await get_user_localization(message.from_user.id)),
                             reply_markup=await show_categories_for_create_question_keyboard(
                                 await get_categories_on_page(user_category_page[message.from_user.id], user_category_father[message.from_user.id]),
                                 user_category_page[message.from_user.id],
                                 await get_categories_page_count(user_category_father[message.from_user.id]),
                                 appeal['id'],
                                 message.from_user.id))
    elif await state.get_state() == "Status:answer":
        await state.finish()
        await insert_message(message.from_user.id, user_answer_to[message.from_user.id], message.text, False)
        notices = await get_appeal_notices_managers(user_answer_to[message.from_user.id])
        await del_appeal_notices_managers(user_answer_to[message.from_user.id])
        for notice in notices:
            await bot.delete_message(notice["user_id"], notice["message_id"])
        appeal = await get_appeal(user_answer_to[message.from_user.id])
        admin = await get_user_info(appeal['manager_id'])
        user = await get_user_info(appeal["user_id"])
        await message.answer(await _("Сообщение отправлено, ожидайте ответа менеджера!", user['localization']))
        await del_appeal_notices_managers(user_answer_to[message.from_user.id])
        msg = await bot.send_message(appeal['manager_id'],
                                     text=f"{await _('⚠️ Новое сообщение в чате ⚠️', admin['localization'])}\n"
                                          f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
                                          f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
                                          f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
                                          f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
                                     reply_markup=await manager_appeal_in_work_keyboard(appeal["id"],
                                                                                        appeal['manager_id'], user["blocked"]))
        await insert_appeal_notice(user_answer_to[message.from_user.id], appeal['manager_id'], msg.message_id, True)
    elif await state.get_state() == "Status:find_user":
        await state.finish()
        user = await get_user_by_username(message.text)
        if user is None:
            await message.answer(await _('Пользователь не найден', await get_user_localization(message.from_user.id)),
                                 reply_markup=await close_keyboard(message.from_user.id))
        else:
            answer_text = await _('Пользователь', await get_user_localization(message.from_user.id)) + ": @" + user["nickname"] + "\n"
            answer_text += await _('Дата регистрации', await get_user_localization(message.from_user.id)) + ": " + str(user["date_registration"].strftime("%Y-%m-%d %H:%M")) + "\n"
            answer_text += await _('Язык', await get_user_localization(message.from_user.id)) + ": " + user["localization"] + "\n"
            if user["blocked"]:
                answer_text += await _('Заблокирован', await get_user_localization(message.from_user.id)) + "\n"
            await message.answer(answer_text,
                                 reply_markup=await user_find_keyboard(user["blocked"], user["user_id"], message.from_user.id))
    else:
        await state.finish()
        await message.answer(
            await _("Вы прислали необрабатываемое сообщение или не отвечали более суток\nВыберите пункт из меню снизу",
                    await get_user_localization(message.from_user.id)),
            reply_markup=await main_keyboard(message.from_user.id))
