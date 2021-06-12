from django.conf import settings
from tortoise import Tortoise

from apps.bot import app_name as bot_name
from apps.hiring import app_name as hiring_name


async def init():
    await Tortoise.init(
        db_url=settings.PG_URL,
        modules={
            f'{bot_name}': ['apps.bot.tortoise_models'],
            f'{hiring_name}': ['apps.hiring.tortoise_models']
        }
    )


async def start_db_connection():
    await init()
