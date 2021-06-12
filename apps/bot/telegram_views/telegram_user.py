import re

from aiogram.types import ContentType

from apps.bot import callback_filters as bot_callback_filters, bot, keyboards, dispatcher as dp, messages, \
    callback_filters
from apps.bot.callback_filters import message_is_not_command, message_is_not_back
from apps.bot.states import TelegramUserForm
from apps.bot.telegram_views.bot import send_main_menu
from apps.bot.tortoise_models import Button, TelegramUser


@dp.message_handler(callback_filters.language_choice, state=TelegramUserForm.language_choice.state)
async def language_choice_processing(message, locale, state):
    user_id = message.from_user.id
    customer = await TelegramUser.get(id=user_id)
    text = message.text
    en_button = await Button.get(code='en')
    ru_button = await Button.get(code='ru')
    language = en_button.code if text == en_button.text_en else ru_button.code if text == ru_button.text_ru else 'uz'
    customer.language = language
    await customer.save()

    await bot.send_message(user_id, '✔', reply_markup=keyboards.remove_keyboard)
    await send_main_menu(customer, language, state)


@dp.message_handler(message_is_not_back, message_is_not_command, state=TelegramUserForm.phone_number.state,
                    content_types=[ContentType.TEXT, ContentType.CONTACT])
async def phone_number_save(message, locale, state):
    user_id = message.from_user.id
    customer = await TelegramUser.get(id=user_id)
    contact = message.contact
    phone_number = contact.phone_number if contact else message.text

    customer.phone_number = phone_number
    await customer.save()

    await bot.send_message(user_id, '✔', reply_markup=keyboards.remove_keyboard)
    await send_main_menu(customer, locale, state)


@dp.message_handler(bot_callback_filters.message_is_not_command, bot_callback_filters.message_is_not_back,
                    state=TelegramUserForm.full_name.state, content_types=[ContentType.TEXT])
async def full_name_save(message, locale, state):
    user_id = message.from_user.id
    customer = await TelegramUser.get(id=user_id)
    full_name = message.text
    customer.full_name = full_name
    await customer.save()

    await bot.send_message(user_id, '✔', reply_markup=keyboards.remove_keyboard)
    await send_main_menu(customer, locale, state)
