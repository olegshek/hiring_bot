from aiogram import types

from apps.bot import dispatcher as dp, messages, bot, callback_filters
from apps.bot import keyboards
from apps.bot.callback_filters import keyboard_back, inline_back
from apps.bot.states import TelegramUserForm, BotForm
from apps.bot.tortoise_models import TelegramUser
from apps.bot.utils import try_delete_message
from apps.hiring.states import HiringForm, prev_resume_states
from apps.hiring.tortoise_models import Resume


async def send_main_menu(customer, locale, state=None):
    if state:
        await state.finish()

    if not customer.full_name:
        await TelegramUserForm.full_name.set()
        return await bot.send_message(
            customer.id,
            await messages.get_message('full_name', locale),
            reply_markup=await keyboards.back_keyboard(locale)
        )

    if not customer.phone_number:
        await TelegramUserForm.phone_number.set()
        return await bot.send_message(
            customer.id,
            await messages.get_message('phone_number', locale),
            reply_markup=await keyboards.phone_number(locale)
        )

    else:
        await BotForm.main_menu.set()
        await bot.send_message(
            customer.id,
            await messages.get_message('main_menu', locale),
            reply_markup=await keyboards.main_menu(locale)
        )


async def back(user_id, state, locale, message_id=None):
    state_name = await state.get_state()
    customer = await TelegramUser.get(id=user_id)

    if state_name == TelegramUserForm.full_name.state:
        await TelegramUserForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, False))

    if state_name == TelegramUserForm.phone_number.state:
        await TelegramUserForm.full_name.set()
        return await bot.send_message(
            customer.id,
            await messages.get_message('full_name', locale),
            reply_markup=await keyboards.back_keyboard(locale)
        )

    if state_name in [HiringForm.categories.state, TelegramUserForm.language_choice.state]:
        if message_id:
            await try_delete_message(user_id, message_id)

        return await send_main_menu(customer, locale, state)

    if state_name == HiringForm.resume_filling.state:
        from apps.hiring.telegram_views import fill_out_resume

        async with state.proxy() as data:
            resume_id = data['resume_id']
            resume_state = data['resume_state']

        resume = await Resume.get(id=resume_id)

        if resume_state == 'email':
            from apps.hiring.telegram_views import send_categories

            if not await Resume.filter(user_id=user_id).exclude(id=resume_id):
                user = await resume.user
                user.email = None
                await user.save()
                await try_delete_message(user_id, message_id)
                return await send_categories(user_id, locale)

            return await send_categories(user_id, locale)

        prev_state = prev_resume_states[resume_state]
        setattr(resume, prev_state, None)
        await resume.save()
        await fill_out_resume(resume, locale, state)

    if state_name == HiringForm.resume_select.state:
        from apps.hiring.telegram_views import send_categories

        await try_delete_message(user_id, message_id)
        await send_categories(user_id, locale)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, locale):
    user_id = message.from_user.id
    customer = await TelegramUser.filter(id=user_id).first()
    if not customer:
        customer = await TelegramUser.create(id=user_id, username=message.from_user.username)

    await bot.send_message(user_id, await messages.get_message('greeting', locale),
                           reply_markup=keyboards.remove_keyboard)

    if not customer.language:
        await TelegramUserForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, False))

    await send_main_menu(customer, locale)


@dp.callback_query_handler(callback_filters.main_menu, state=BotForm.main_menu.state)
async def main_menu(query, locale, state):
    user_id = query.from_user.id
    data = query.data
    message_id = query.message.message_id

    if data in ('submit_resume', 'find_candidate'):
        from apps.hiring.telegram_views import send_categories

        async with state.proxy() as state_data:
            state_data['hiring_type'] = data

        await send_categories(user_id, locale, message_id)

    if data == 'change_language':
        await try_delete_message(user_id, message_id)
        await TelegramUserForm.language_choice.set()
        return await bot.send_message(user_id, await messages.get_message('language_choice', locale),
                                      reply_markup=await keyboards.language_choice(locale, True))


@dp.message_handler(keyboard_back, state='*')
async def button_back(message, state, locale):
    user_id = message.from_user.id

    await bot.send_message(user_id, '🔙', reply_markup=keyboards.remove_keyboard)
    await back(message.from_user.id, state, locale)


@dp.callback_query_handler(inline_back, state='*')
async def back_inline(query, state, locale):
    await back(query.from_user.id, state, locale, query.message.message_id)
