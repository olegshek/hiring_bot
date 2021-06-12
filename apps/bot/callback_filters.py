from apps.bot.tortoise_models import Button
from core.callback_filters import callback_filter


async def keyboard_back(message):
    back_button = await Button.get(code='back')
    return message.text in [getattr(back_button, f'text_{locale}') for locale in ['ru', 'en']]


async def inline_back(query):
    return query.data == 'back'


async def message_is_not_command(message):
    if message.text:
        return not message.text.startswith('/')
    return True


async def message_is_not_back(message):
    back_button = await Button.get(code='back')
    return message.text not in [getattr(back_button, f'text_{locale}') for locale in ['ru', 'en']]


async def language_choice(message):
    en_text = (await Button.get(code='en')).text_en
    ru_text = (await Button.get(code='ru')).text_ru
    return message.text in [en_text, ru_text]


async def main_menu(query):
    return await callback_filter(query, 'main_menu')
