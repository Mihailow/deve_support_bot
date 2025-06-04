from misc import *
from translations import _


# предыдущая стрница категорий
@dp.callback_query_handler(text="show_category_back")
async def but_show_category_back(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    shown_appeals_page_count = await get_shown_appeals_page_count(user_category_father[callback_query.from_user.id])

    if user_category_page[callback_query.from_user.id] > 1:
        user_category_page[callback_query.from_user.id] -= 1

    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    shown_appeals = []
    if not categories:
        shown_appeals = await get_shown_appeals_on_page(
            user_category_page[callback_query.from_user.id] - categories_page_count,
            user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_appeals_keyboard(
                                            categories, shown_appeals, user_category_page[callback_query.from_user.id],
                                            categories_page_count + shown_appeals_page_count,
                                            callback_query.from_user.id))


# следующая стрница категорий
@dp.callback_query_handler(text="show_category_next")
async def but_show_category_next(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    shown_appeals_page_count = await get_shown_appeals_page_count(user_category_father[callback_query.from_user.id])

    if user_category_page[callback_query.from_user.id] < categories_page_count + shown_appeals_page_count:
        user_category_page[callback_query.from_user.id] += 1

    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    shown_appeals = []
    if not categories:
        shown_appeals = await get_shown_appeals_on_page(
            user_category_page[callback_query.from_user.id] - categories_page_count,
            user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_appeals_keyboard(
                                            categories, shown_appeals, user_category_page[callback_query.from_user.id],
                                            categories_page_count + shown_appeals_page_count,
                                            callback_query.from_user.id))


# предыдущая стрница категорий при создании вопроса
@dp.callback_query_handler(text_startswith="show_category_back_", state=Status.choose_category)
async def but_show_category_back_choose_category(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])

    if user_category_page[callback_query.from_user.id] > 1:
        user_category_page[callback_query.from_user.id] -= 1

    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_for_create_question_keyboard(
                                            categories, user_category_page[callback_query.from_user.id],
                                            categories_page_count, callback_query.data[19:],
                                            callback_query.from_user.id))


# следующая стрница категорий при создании вопроса
@dp.callback_query_handler(text_startswith="show_category_next_", state=Status.choose_category)
async def but_show_category_next_choose_category(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    if user_category_page[callback_query.from_user.id] < categories_page_count:
        user_category_page[callback_query.from_user.id] += 1
    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_for_create_question_keyboard(
                                            categories, user_category_page[callback_query.from_user.id],
                                            categories_page_count, callback_query.data[19:],
                                            callback_query.from_user.id))


# переход к просмотру вопросов в категории
@dp.callback_query_handler(text_startswith="show_category_number_")
async def but_show_category_number_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    user_category_page[callback_query.from_user.id] = 1
    user_category_father[callback_query.from_user.id] = callback_query.data[21:]
    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    shown_appeals = []
    shown_appeals_page_count = await get_shown_appeals_page_count(user_category_father[callback_query.from_user.id])
    if not categories:
        shown_appeals = await get_shown_appeals_on_page(
            user_category_page[callback_query.from_user.id] - categories_page_count,
            user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_appeals_keyboard(
                                            categories, shown_appeals, user_category_page[callback_query.from_user.id],
                                            categories_page_count + shown_appeals_page_count,
                                            callback_query.from_user.id))


# переход к просмотру вопросов в категории
@dp.callback_query_handler(text_startswith="show_category_number_", state=Status.choose_category)
async def but_show_category_number_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data[21:].split("_")
    data = {
        "category_id": data[0],
        "appeal_id": data[1],
    }
    user_category_page[callback_query.from_user.id] = 1
    user_category_father[callback_query.from_user.id] = data["category_id"]
    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_for_create_question_keyboard(
                                            categories, user_category_page[callback_query.from_user.id],
                                            categories_page_count, data["appeal_id"],
                                            callback_query.from_user.id))


# переход к просмотру вопроса
@dp.callback_query_handler(text_startswith="shown_appeal_number_")
async def but_shown_appeal_number_(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    appeal = await get_shown_appeals(callback_query.data[20:])
    await callback_query.message.answer(f"{appeal['question_text']}\n\n"
                                        f"{appeal['answer_text']}",
                                        reply_markup=await look_shown_appeal_keyboard(callback_query.from_user.id))


# вернуться к выбору категорий
@dp.callback_query_handler(text="back_to_show_categories")
async def but_back_to_show_categories(callback_query: types.CallbackQuery):
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
    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    shown_appeals = []
    shown_appeals_page_count = await get_shown_appeals_page_count(user_category_father[callback_query.from_user.id])
    if not categories:
        shown_appeals = await get_shown_appeals_on_page(
            user_category_page[callback_query.from_user.id] - categories_page_count,
            user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_appeals_keyboard(
                                            categories, shown_appeals, user_category_page[callback_query.from_user.id],
                                            categories_page_count + shown_appeals_page_count,
                                            callback_query.from_user.id))


@dp.callback_query_handler(text_startswith="back_to_show_categories_", state=Status.choose_category)
async def but_back_to_show_categories(callback_query: types.CallbackQuery):
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
    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_for_create_question_keyboard(
                                            categories, user_category_page[callback_query.from_user.id],
                                            categories_page_count, callback_query.data[24:],
                                            callback_query.from_user.id))


# вернуться к выбору категорий
@dp.callback_query_handler(text="back_to_show_categories_from_appeal")
async def but_back_to_show_categories_from_appeal(callback_query: types.CallbackQuery):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    categories = await get_categories_on_page(user_category_page[callback_query.from_user.id],
                                              user_category_father[callback_query.from_user.id])
    categories_page_count = await get_categories_page_count(user_category_father[callback_query.from_user.id])
    shown_appeals = []
    shown_appeals_page_count = await get_shown_appeals_page_count(user_category_father[callback_query.from_user.id])
    if not categories:
        shown_appeals = await get_shown_appeals_on_page(
            user_category_page[callback_query.from_user.id] - categories_page_count,
            user_category_father[callback_query.from_user.id])
    await callback_query.message.answer(await _("Выберите категорию", await get_user_localization(callback_query.from_user.id)),
                                        reply_markup=await show_categories_appeals_keyboard(
                                            categories, shown_appeals, user_category_page[callback_query.from_user.id],
                                            categories_page_count + shown_appeals_page_count,
                                            callback_query.from_user.id))


# создать вопрос
@dp.callback_query_handler(text="create_appeal")
async def but_create_appeal(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    time = await get_last_unfinished_user_appeal(callback_query.from_user.id)
    if time:
        time = datetime.now() - time["date_create"]
        min_time_between_appeals = timedelta(seconds=await get_setting("min_time_between_appeals"))
        if time < min_time_between_appeals:
            time = min_time_between_appeals - time
            await callback_query.message.answer(
                f"{await _('Вы превысили лимит вопросов, подождите', await get_user_localization(callback_query.from_user.id))}"
                f" {time.seconds} {await _('секунд', await get_user_localization(callback_query.from_user.id))}",
                reply_markup=await main_keyboard(callback_query.from_user.id))
            return
    if await get_user_appeals_count(callback_query.from_user.id) >= await get_setting("max_count_appeals"):
        await callback_query.message.answer(await _("Вы превысили лимит необработанных вопросов",
                                                    await get_user_localization(callback_query.from_user.id)),
                                            reply_markup=await main_keyboard(callback_query.from_user.id))
    else:
        await state.set_state(Status.create_appeal)
        await callback_query.message.answer(
            await _("Напишите интересующий вас вопрос", await get_user_localization(callback_query.from_user.id)),
            reply_markup=await close_keyboard(callback_query.from_user.id))


# отправить категорию вопроса при создании вопроса
@dp.callback_query_handler(text_startswith="set_category_number_", state=Status.choose_category)
async def but_set_category_number__choose_category(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await state.finish()
    del (user_category_page[callback_query.from_user.id])
    data = callback_query.data[20:].split("_")
    data = {
        "category_id": data[0],
        "appeal_id": data[1],
    }
    await update_appeal_category_user(data["category_id"], data["appeal_id"])
    await update_pre_message(data["appeal_id"])
    await callback_query.message.answer(await _("Создан новый запрос, ожидайте ответа менеджера!",
                                                await get_user_localization(callback_query.from_user.id)))
    appeal = await get_appeal(data["appeal_id"])
    user = await get_user_info(callback_query.from_user.id)
    category_id = await get_category_main_father(data["category_id"])
    await send_to_admins(await get_managers_id(category_id), appeal["id"], appeal["appeal_id"],
                         await get_category_name(appeal["category_id"]), appeal["question_text"], user["nickname"])


# ответить менеджеру
@dp.callback_query_handler(text_startswith="answer_", state="*")
async def but_answer_(callback_query: types.CallbackQuery, state: FSMContext):
    if await get_user_is_blocked(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, await _("Вы заблокированы", await get_user_localization(callback_query.from_user.id)))
        return
    if await get_setting("status") == "выключен":
        await bot.send_message(callback_query.from_user.id, await _("К сожалению, бот временно недоступен", await get_user_localization(callback_query.from_user.id)))
        return
    appeal = await get_appeal(callback_query.data[7:])
    if appeal["status"] == "Завершено":
        await callback_query.message.answer(
            await _("Обращение закрыто", await get_user_localization(callback_query.from_user.id)))
        return
    await state.finish()
    await state.set_state(Status.answer)
    user_answer_to[callback_query.from_user.id] = callback_query.data[7:]
    await callback_query.message.answer(
        await _("Введите сообщение для отправки менеджеру", await get_user_localization(callback_query.from_user.id)),
        reply_markup=await close_keyboard(callback_query.from_user.id))
