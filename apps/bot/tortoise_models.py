from enum import Enum

from django.utils import timezone
from tortoise import models, fields

from apps.bot import app_name


class Button(models.Model):
    code = fields.CharField(max_length=50, unique=True)
    text = fields.CharField(max_length=50, unique=True)
    text_ru = fields.CharField(max_length=50, unique=True)
    text_en = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = f'{app_name}_button'


class Keyboard(models.Model):
    code = fields.CharField(max_length=50, unique=True)
    buttons = fields.ManyToManyField('bot.Button', related_name='keyboards', through='bot_keyboardbuttonsordering',
                                     forward_key='button_id', backward_key='keyboard_id')

    class Meta:
        table = f'{app_name}_keyboard'


class KeyboardButtonsOrdering(models.Model):
    keyboard = fields.ForeignKeyField('bot.Keyboard', on_delete=fields.CASCADE, related_name='buttons_ordering')
    button = fields.ForeignKeyField('bot.Button', on_delete=fields.CASCADE, related_name='ordering')
    ordering = fields.SmallIntField()

    class Meta:
        table = f'{app_name}_keyboardbuttonsordering'


class Message(models.Model):
    code = fields.CharField(max_length=100, unique=True)
    text_ru = fields.TextField()
    text_en = fields.TextField()

    class Meta:
        table = f'{app_name}_message'


class TelegramUser(models.Model):
    class Languages(str, Enum):
        RU = 'ru'
        EN = 'en'

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, blank=True, null=True)
    full_name = fields.CharField(max_length=200, null=True, blank=True)
    phone_number = fields.CharField(max_length=20, null=True)
    email = fields.CharField(max_length=200, null=True)
    language = fields.CharField(max_length=2, choices=Languages, null=True)

    created_at = fields.DatetimeField(default=timezone.now)

    class Meta:
        table = f'{app_name}_telegramuser'