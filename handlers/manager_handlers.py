from misc import *
from translations import _


# предыдущая стрница категорий при изменении категории
@dp.callback_query_handler(text_startswith="change_category_back_", state=Status.change_category)
async def but_change_category_back_change_category(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if user_category_page[callback_query.from_user.id] > 1:
        user_category_page[callback_query.from_user.id] -= 1
    await callback_query.message.answer(
        await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await manager_change_category_keyboard(
            await get_categories_on_page(user_category_page[callback_query.from_user.id], user_category_father[callback_query.from_user.id]),
            user_category_page[callback_query.from_user.id],
            await get_categories_page_count(user_category_father[callback_query.from_user.id]),
            callback_query.data[21:],
            callback_query.from_user.id))


# следующая стрница категорий при изменении категории
@dp.callback_query_handler(text_startswith="change_category_next_", state=Status.change_category)
async def but_change_category_next_change_category(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if user_category_page[callback_query.from_user.id] < await get_categories_page_count(user_category_father[callback_query.from_user.id]):
        user_category_page[callback_query.from_user.id] += 1
    await callback_query.message.answer(
        await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await manager_change_category_keyboard(
            await get_categories_on_page(user_category_page[callback_query.from_user.id], user_category_father[callback_query.from_user.id]),
            user_category_page[callback_query.from_user.id],
            await get_categories_page_count(user_category_father[callback_query.from_user.id]),
            callback_query.data[21:],
            callback_query.from_user.id))


# следующая стрница категорий при изменении категории
@dp.callback_query_handler(text_startswith="show_change_category_number_", state=Status.change_category)
async def but_change_category_next_change_category(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[28:].split("_")
    data = {
        "category_id": data[0],
        "appeal_id": data[1],
    }
    user_category_page[callback_query.from_user.id] = 1
    user_category_father[callback_query.from_user.id] = data["category_id"]
    await callback_query.message.answer(
        await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await manager_change_category_keyboard(
            await get_categories_on_page(user_category_page[callback_query.from_user.id], user_category_father[callback_query.from_user.id]),
            user_category_page[callback_query.from_user.id],
            await get_categories_page_count(user_category_father[callback_query.from_user.id]),
            data["appeal_id"],
            callback_query.from_user.id))


# предыдущая стрница вопросов
@dp.callback_query_handler(text_startswith="manager_appeal_back_")
async def but_manager_appeal_back_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if user_appeal_page[callback_query.from_user.id] > 1:
        user_appeal_page[callback_query.from_user.id] -= 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await managers_appeals_keyboard(
            await get_appeals_on_page(user_appeal_page[callback_query.from_user.id],
                                      callback_query.from_user.id,
                                      callback_query.data[20:], await get_is_admin(callback_query.from_user.id)),
            user_appeal_page[callback_query.from_user.id],
            await get_appeals_page_count(callback_query.from_user.id,
                                         callback_query.data[20:], await get_is_admin(callback_query.from_user.id)),
            callback_query.data[20:],
            callback_query.from_user.id))


# следующая стрница вопросов
@dp.callback_query_handler(text_startswith="manager_appeal_next_")
async def but_manager_appeal_next_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if user_appeal_page[callback_query.from_user.id] < await get_appeals_page_count(callback_query.from_user.id,
                                                                                    callback_query.data[20:],
                                                                                    await get_is_admin(callback_query.from_user.id)):
        user_appeal_page[callback_query.from_user.id] += 1
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await managers_appeals_keyboard(
            await get_appeals_on_page(user_appeal_page[callback_query.from_user.id],
                                      callback_query.from_user.id,
                                      callback_query.data[20:], await get_is_admin(callback_query.from_user.id)),
            user_appeal_page[callback_query.from_user.id],
            await get_appeals_page_count(callback_query.from_user.id,
                                         callback_query.data[20:], await get_is_admin(callback_query.from_user.id)),
            callback_query.data[20:],
            callback_query.from_user.id))


# отправить категорию вопроса при изменении категории
@dp.callback_query_handler(text_startswith="change_category_number_", state=Status.change_category)
async def but_change_category_number_change_category(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[23:].split("_")
    data = {
        "category_id": data[0],
        "appeal_id": data[1],
    }
    await update_appeal_category_admin(data["appeal_id"], data["category_id"])
    notices = await get_appeal_notices_managers(data["appeal_id"])
    await del_appeal_notices_managers(data["appeal_id"])
    for notice in notices:
        await bot.delete_message(notice["user_id"], notice["message_id"])
    appeal = await get_appeal(data["appeal_id"])
    user = await get_user_info(appeal["user_id"])
    category_id = await get_category_main_father(data["category_id"])
    await send_to_admins(await get_managers_id(category_id), appeal["id"], appeal["appeal_id"],
                         await get_category_name(appeal["category_id"]), appeal["question_text"], user["nickname"])


# вернуться к выбору категорий
@dp.callback_query_handler(text_startswith="back_to_show_categories_", state=Status.change_category)
async def but_back_to_show_categories_change_category(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if user_category_father[callback_query.from_user.id] == 0:
        del(user_category_page[callback_query.from_user.id])
        del(user_category_father[callback_query.from_user.id])
        return
    user_category_page[callback_query.from_user.id] = 1
    user_category_father[callback_query.from_user.id] = await get_category_father(user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(
        await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await manager_change_category_keyboard(
            await get_categories_on_page(user_category_page[callback_query.from_user.id], user_category_father[callback_query.from_user.id]),
            user_category_page[callback_query.from_user.id],
            await get_categories_page_count(user_category_father[callback_query.from_user.id]),
            callback_query.data[24:],
            callback_query.from_user.id))


# переход к просмотру вопроса
@dp.callback_query_handler(text_startswith="manager_appeal_number_")
async def but_show_appeal_number_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[22:].split("_")
    data = {
        "category_id": data[0],
        "appeal_id": data[1],
    }
    appeal = await get_appeal(data["category_id"])
    admin = await get_user_info(callback_query.from_user.id)
    user = await get_user_info(appeal["user_id"])
    await callback_query.message.answer(text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
                                             f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
                                             f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
                                             f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
                                        reply_markup=await managers_appeals_back_keyboard(callback_query.from_user.id,
                                                                                          data["appeal_id"]))


# взять в работу
@dp.callback_query_handler(text_startswith="take_in_work_", state="*")
async def but_take_in_work(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    notices = await get_appeal_notices_managers(callback_query.data[13:])
    await del_appeal_notices_managers(callback_query.data[13:])
    for notice in notices:
        await bot.delete_message(notice["user_id"], notice["message_id"])
    await update_appeal_admin(callback_query.from_user.id, callback_query.data[13:], "В работе")
    appeal = await get_appeal(callback_query.data[13:])
    admin = await get_user_info(callback_query.from_user.id)
    user = await get_user_info(appeal["user_id"])
    msg = await callback_query.message.answer(
        text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
             f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
             f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
             f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
        reply_markup=await manager_appeal_in_work_keyboard(appeal["id"], callback_query.from_user.id, user["blocked"]))
    await insert_appeal_notice(callback_query.data[13:], callback_query.from_user.id, msg.message_id, True)
    await insert_message(callback_query.from_user.id, callback_query.data[13:], "Ваше обращение принято в работу", True)
    await bot.send_message(user["user_id"], await _('Ваше обращение принято в работу', user['localization']))


# изменить категорию вопроса
@dp.callback_query_handler(text_startswith="change_appeal_category_", state="*")
async def but_change_appeal_category_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await state.set_state(Status.change_category)
    user_category_page[callback_query.from_user.id] = 1
    user_category_father[callback_query.from_user.id] = 0
    await callback_query.message.answer(
        await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await manager_change_category_keyboard(
            await get_categories_on_page(user_category_page[callback_query.from_user.id], user_category_father[callback_query.from_user.id]),
            user_category_page[callback_query.from_user.id],
            await get_categories_page_count(user_category_father[callback_query.from_user.id]),
            callback_query.data[23:],
            callback_query.from_user.id))


# предложить закрыть обращение
@dp.callback_query_handler(text_startswith="suggest_closing_", state="*")
async def but_suggest_closing_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    appeal = await get_appeal(callback_query.data[16:])
    admin = await get_user_info(appeal['manager_id'])
    user = await get_user_info(appeal["user_id"])
    await del_appeal_notices_managers(appeal['id'])
    msg = await callback_query.message.answer(
        text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
             f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
             f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
             f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
        reply_markup=await manager_appeal_in_work_close_keyboard(appeal["id"], callback_query.from_user.id, user["blocked"]))
    await insert_appeal_notice(callback_query.data[16:], appeal['manager_id'], msg.message_id, True)
    msg = await bot.send_message(user["user_id"], await _("Ваш вопрос решён?",
                                                          user["localization"]),
                                 reply_markup=await new_message_keyboard(callback_query.data[16:],
                                                                         user["user_id"]))
    await insert_appeal_notice(callback_query.data[16:], user["user_id"], msg.message_id, False)


# изменить менеджера
@dp.callback_query_handler(text_startswith="change_appeal_manager_", state="*")
async def but_change_appeal_manager_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await update_appeal_admin(None, callback_query.data[22:], "Создано")
    appeal = await get_appeal(callback_query.data[22:])
    user = await get_user_info(appeal["user_id"])
    category_id = await get_category_main_father(appeal["category_id"])
    await send_to_admins(await get_managers_id(category_id), appeal["id"], appeal["appeal_id"],
                         await get_category_name(appeal["category_id"]),
                         appeal["question_text"], user["nickname"], callback_query.from_user.id)


# назад к выбору обращения
@dp.callback_query_handler(text_startswith="back_to_managers_appears_", state="*")
async def but_back_to_managers_appears_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(
        await _("Выберите номер обращения", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await managers_appeals_keyboard(
            await get_appeals_on_page(user_appeal_page[callback_query.from_user.id],
                                      callback_query.from_user.id,
                                      callback_query.data[25:], await get_is_admin(callback_query.from_user.id)),
            user_appeal_page[callback_query.from_user.id],
            await get_appeals_page_count(callback_query.from_user.id,
                                         callback_query.data[25:], await get_is_admin(callback_query.from_user.id)),
            callback_query.data[25:],
            callback_query.from_user.id,))


# заблокировать пользователя
@dp.callback_query_handler(text_startswith="block_user_owner_", state="*")
async def but_block_user_owner_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    appeal = await get_appeal(callback_query.data[17:])
    await update_user_blocked(appeal["user_id"])
    notices = await get_appeal_notices_managers(appeal["id"])
    await del_appeal_notices_managers(appeal["id"])
    for notice in notices:
        await bot.delete_message(notice["user_id"], notice["message_id"])
    admin = await get_user_info(callback_query.from_user.id)
    user = await get_user_info(appeal["user_id"])
    msg = await callback_query.message.answer(
        text=f"{await _('Обращение', admin['localization'])}: #{appeal['appeal_id']}\n"
             f"{await _('Категория', admin['localization'])}: {await get_category_name(appeal['category_id'])}\n"
             f"{await _('Сообщение', admin['localization'])}: {appeal['question_text']}\n"
             f"{await _('Пользователь', admin['localization'])}: @{user['nickname']}",
        reply_markup=await manager_appeal_in_work_keyboard(appeal["id"], callback_query.from_user.id, user["blocked"]))
    await insert_appeal_notice(appeal["id"], callback_query.from_user.id, msg.message_id, True)
