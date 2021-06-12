from aiogram.dispatcher.filters.state import StatesGroup, State


class BotForm(StatesGroup):
    main_menu = State()


class TelegramUserForm(StatesGroup):
    language_choice = State()
    phone_number = State()
    full_name = State()
    email = State()
    contact_manager = State()