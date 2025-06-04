from misc import *
from translations import _


# переход к просмотру вопроса
@dp.callback_query_handler(text_startswith="user_appeal_number_")
async def but_show_appeal_number_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[19:].split("_")
    data = {
        "appeal_id": data[0],
        "status": data[1],
    }
    appeal = await get_appeal(data["appeal_id"])
    admin = await get_user_info(callback_query.from_user.id)
    user = await get_user_info(appeal["user_id"])
    await callback_query.message.answer(text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
                                             f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
                                             f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
                                             f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
                                        reply_markup=await user_appeals_back_keyboard(callback_query.from_user.id,
                                                                                      data["status"], appeal["user_id"]))


# заблокировать пользователя
@dp.callback_query_handler(text_startswith="block_user_", state="*")
async def but_block_user_owner_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await update_user_blocked(callback_query.data[11:])
    user = await get_user_info(callback_query.data[11:])
    answer_text = await _('Пользователь', await get_user_localization(callback_query.from_user.id)) + ": @" + user[
        "nickname"] + "\n"
    answer_text += await _('Дата регистрации', await get_user_localization(callback_query.from_user.id)) + ": " + str(
        user["date_registration"].strftime("%Y-%m-%d %H:%M")) + "\n"
    answer_text += await _('Язык', await get_user_localization(callback_query.from_user.id)) + ": " + user[
        "localization"] + "\n"
    if user["blocked"]:
        answer_text += await _('Заблокирован', await get_user_localization(callback_query.from_user.id)) + "\n"
    await callback_query.message.answer(answer_text,
                                        reply_markup=await user_find_keyboard(user["blocked"],
                                                                              user["user_id"],
                                                                              callback_query.from_user.id))


@dp.callback_query_handler(text_startswith="back_to_user_find_", state="*")
async def but_back_to_user_find_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await state.finish()
    user = await get_user_info(callback_query.data[18:])
    answer_text = await _('Пользователь', await get_user_localization(callback_query.from_user.id)) + ": @" + user[
        "nickname"] + "\n"
    answer_text += await _('Дата регистрации', await get_user_localization(callback_query.from_user.id)) + " " + str(
        user["date_registration"].strftime("%Y-%m-%d %H:%M")) + "\n"
    answer_text += await _('Язык', await get_user_localization(callback_query.from_user.id)) + " " + user[
        "localization"] + "\n"
    if user["blocked"]:
        answer_text += await _('Заблокирован', await get_user_localization(callback_query.from_user.id)) + "\n"
    await callback_query.message.answer(answer_text,
                                        reply_markup=await user_find_keyboard(user["blocked"],
                                                                              user["user_id"],
                                                                              callback_query.from_user.id))


@dp.callback_query_handler(text_startswith="back_to_user_appears_", state="*")
async def but_back_to_user_appears_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[21:].split("_")
    data = {
        "status": data[0],
        "find_user_id": data[1],
    }
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_appeals_keyboard(
            await get_user_appeals_on_page(user_appeal_page[callback_query.from_user.id], data["find_user_id"],
                                           data["status"]),
            user_appeal_page[callback_query.from_user.id],
            await get_user_appeals_page_count(data["find_user_id"], data["status"]),
            data["status"],
            data["find_user_id"],
            callback_query.from_user.id))


# назад к admin
@dp.callback_query_handler(text="back_to_admin", state="*")
async def but_back_to_admin(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await send_admin_text(callback_query.from_user.id, await get_setting("owner_id"), await get_manager(callback_query.from_user.id))


# предыдущая стрница вопросов
@dp.callback_query_handler(text_startswith="user_appeal_back_")
async def but_appeal_back_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[17:].split("_")
    data = {
        "status": data[0],
        "find_user_id": data[1],
    }
    if user_appeal_page[callback_query.from_user.id] > 1:
        user_appeal_page[callback_query.from_user.id] -= 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_appeals_keyboard(
            await get_user_appeals_on_page(user_appeal_page[callback_query.from_user.id], data["find_user_id"], data["status"]),
            user_appeal_page[callback_query.from_user.id],
            await get_user_appeals_page_count(data["find_user_id"], data["status"]),
            data["status"],
            data["find_user_id"],
            callback_query.from_user.id))


# следующая стрница вопросов
@dp.callback_query_handler(text_startswith="user_appeal_next_")
async def but_user_appeal_next_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[17:].split("_")
    data = {
        "status": data[0],
        "find_user_id": data[1],
    }
    if user_appeal_page[callback_query.from_user.id] < await get_user_appeals_page_count(callback_query.from_user.id, data["status"]):
        user_appeal_page[callback_query.from_user.id] += 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_appeals_keyboard(
            await get_user_appeals_on_page(user_appeal_page[callback_query.from_user.id], data["find_user_id"], data["status"]),
            user_appeal_page[callback_query.from_user.id],
            await get_user_appeals_page_count(data["find_user_id"], data["status"]),
            data["status"],
            data["find_user_id"],
            callback_query.from_user.id))


# показать активные обращения менеджера
@dp.callback_query_handler(text="show_active_appeals")
async def but_show_active_appeals(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_appeal_page[callback_query.from_user.id] = 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await managers_appeals_keyboard(
            await get_appeals_on_page(user_appeal_page[callback_query.from_user.id],
                                      callback_query.from_user.id,
                                      "В работе", await get_is_admin(callback_query.from_user.id)),
            user_appeal_page[callback_query.from_user.id],
            await get_appeals_page_count(callback_query.from_user.id,
                                         "В работе", await get_is_admin(callback_query.from_user.id)),
            "В работе",  callback_query.from_user.id, ))


# показать активные обращения пользователя
@dp.callback_query_handler(text_startswith="user_active_appeals_")
async def but_user_active_appeals_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_appeal_page[callback_query.from_user.id] = 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_appeals_keyboard(
            await get_user_appeals_on_page(user_appeal_page[callback_query.from_user.id], callback_query.data[20:], "В работе"),
            user_appeal_page[callback_query.from_user.id],
            await get_user_appeals_page_count(callback_query.data[20:], "В работе"),
            "В работе", callback_query.data[20:], callback_query.from_user.id))


# показать новые обращения менеджера
@dp.callback_query_handler(text="show_new_appeals")
async def but_show_new_appeals(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_appeal_page[callback_query.from_user.id] = 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await managers_appeals_keyboard(
            await get_appeals_on_page(user_appeal_page[callback_query.from_user.id],
                                      callback_query.from_user.id,
                                      "Создано", await get_is_admin(callback_query.from_user.id)),
            user_appeal_page[callback_query.from_user.id],
            await get_appeals_page_count(callback_query.from_user.id,
                                         "Создано", await get_is_admin(callback_query.from_user.id)),
            "Создано",  callback_query.from_user.id, ))


# показать новые обращения пользователя
@dp.callback_query_handler(text_startswith="user_new_appeals_")
async def but_user_new_appeals_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_appeal_page[callback_query.from_user.id] = 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_appeals_keyboard(
            await get_user_appeals_on_page(user_appeal_page[callback_query.from_user.id], callback_query.data[17:], "Создано"),
            user_appeal_page[callback_query.from_user.id],
            await get_user_appeals_page_count(callback_query.data[17:], "Создано"),
            "Создано", callback_query.data[17:], callback_query.from_user.id))


# показать закрытые обращения менеджера
@dp.callback_query_handler(text="show_close_appeals")
async def but_show_close_appeals(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_appeal_page[callback_query.from_user.id] = 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await managers_appeals_keyboard(
            await get_appeals_on_page(user_appeal_page[callback_query.from_user.id],
                                      callback_query.from_user.id,
                                      "Завершено", await get_is_admin(callback_query.from_user.id)),
            user_appeal_page[callback_query.from_user.id],
            await get_appeals_page_count(callback_query.from_user.id,
                                         "Завершено", await get_is_admin(callback_query.from_user.id)),
            "Завершено",  callback_query.from_user.id, ))


# показать закрытые обращения пользователя
@dp.callback_query_handler(text_startswith="user_close_appeals_")
async def but_user_close_appeals_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_appeal_page[callback_query.from_user.id] = 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_appeals_keyboard(
            await get_user_appeals_on_page(user_appeal_page[callback_query.from_user.id], callback_query.data[19:], "Завершено"),
            user_appeal_page[callback_query.from_user.id],
            await get_user_appeals_page_count(callback_query.data[19:], "Завершено"),
            "Завершено", callback_query.data[19:], callback_query.from_user.id))


# настройки пользователей
@dp.callback_query_handler(text="user_settings")
async def but_user_settings(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(
        await _("Управление пользователями", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await user_settings_keyboard(callback_query.from_user.id))


# настройки рассылки
@dp.callback_query_handler(text="mailing_settings")
async def but_mailing_settings(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(await _("Добро пожаловать а меню управления рассылками",
                                                await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await mailing_settings_keyboard(await get_all_mailling_from_db(), callback_query.from_user.id))


# настройки пользователя по username
@dp.callback_query_handler(text="find_user_by_id")
async def but_find_user_by_id(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await state.set_state(Status.find_user)
    await callback_query.message.answer(await _("Введите username пользователя", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await back_to_admin_keyboard(callback_query.from_user.id))


# /admin
@dp.message_handler(commands=["admin"], state="*")
async def command_admin(message: types.Message, state: FSMContext):
    if await get_user_is_blocked(message.from_user.id):
        await bot.send_message(message.from_user.id, await _("Вы заблокированы", await get_user_localization(message.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(message.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(message.from_user.id)))
        return
    await update_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.id)
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
    await send_admin_text(message.from_user.id, await get_setting("owner_id"), await get_manager(message.from_user.id))
