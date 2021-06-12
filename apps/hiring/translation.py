from modeltranslation import translator

from apps.bot.models import Button, Message
from apps.hiring.models import Category
from core.translation import TranslationOptionsMixin


@translator.register(Category)
class CategoryOptions(TranslationOptionsMixin):
    fields = ('name', )
