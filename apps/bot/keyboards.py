from aiogram import types

from apps.bot.tortoise_models import Button, KeyboardButtonsOrdering

remove_keyboard = types.ReplyKeyboardRemove()


async def get_back_button_obj():
    return await Button.get(code='back')


async def add_back_inline_button(keyboard, locale):
    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.InlineKeyboardButton(getattr(back_button_obj, f'text_{locale}'), callback_data=back_button_obj.code)
    )
    return keyboard


async def add_back_reply_button(keyboard, locale):
    back_button_obj = await get_back_button_obj()
    keyboard.add(
        types.KeyboardButton(getattr(back_button_obj, f'text_{locale}'))
    )
    return keyboard


async def language_choice(locale='ru', change=False):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='language_choice').order_by(
            'ordering'):
        button = await keyboard_button.button
        code = button.code
        buttons.append(types.InlineKeyboardButton(
            button.text_ru if code == 'ru' else button.text_uz if code == 'uz' else button.text_en
        ))

    if change:
        back_button_obj = await get_back_button_obj()
        buttons.append(types.KeyboardButton(getattr(back_button_obj, f'text_{locale}')))

    keyboard.add(*buttons)
    return keyboard


async def phone_number(locale):
    back_button_obj = await get_back_button_obj()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='phone_number').order_by('ordering'):
        button = await keyboard_button.button
        keyboard.add(types.KeyboardButton(
            getattr(button, f'text_{locale}'),
            request_contact=True if button.code == 'phone_number' else None
        ))
    keyboard.add(types.KeyboardButton(getattr(back_button_obj, f'text_{locale}')))
    return keyboard


async def back_keyboard(locale):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = await get_back_button_obj()
    keyboard.add(types.KeyboardButton(getattr(button, f'text_{locale}')))
    return keyboard


async def main_menu(locale):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='main_menu').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.InlineKeyboardButton(
            getattr(button, f'text_{locale}'),
            callback_data=button.code
        )
        buttons.append(tg_button)

    keyboard.add(*buttons)

    return keyboard


async def categories(category_list, locale):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    buttons = []
    for category in category_list:
        tg_button = types.InlineKeyboardButton(
            getattr(category, f'name_{locale}'),
            callback_data=f'category:{category.id}'
        )
        buttons.append(tg_button)

    keyboard.add(*buttons)
    await add_back_inline_button(keyboard, locale)
    return keyboard


async def yes_or_no(locale):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    buttons = []
    for keyboard_button in await KeyboardButtonsOrdering.filter(keyboard__code='yes_or_no').order_by('ordering'):
        button = await keyboard_button.button
        tg_button = types.KeyboardButton(getattr(button, f'text_{locale}'))
        buttons.append(tg_button)

    keyboard.add(*buttons)
    await add_back_reply_button(keyboard, locale)
    return keyboard


async def resume_menu(resume_id, locale, resumes_quantity, resume_number):
    keyboard = types.InlineKeyboardMarkup(row_width=3)

    switch_buttons = []
    for switch, lookups in zip(['◀️', f'{resume_number}/{resumes_quantity}', '▶️'], ['gte', 'ignore', 'lte']):
        switch_buttons.append(types.InlineKeyboardButton(switch, callback_data=f'{resume_id};{lookups}'))

    keyboard.row(*switch_buttons)

    request_button = await Button.get(code='send_request')
    tg_button = types.InlineKeyboardButton(getattr(request_button, f'text_{locale}'),
                                           callback_data=f'{request_button.code};{resume_id}')
    keyboard.row(tg_button)

    await add_back_inline_button(keyboard, locale)

    return keyboard

