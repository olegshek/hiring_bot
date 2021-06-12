from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config import settings


class Button(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    text = models.CharField(max_length=50, unique=True, verbose_name=_('Text'))

    class Meta:
        verbose_name = _('Button')
        verbose_name_plural = _('Buttons')

    def __str__(self):
        return self.code


class Keyboard(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    buttons = models.ManyToManyField(Button, related_name='keyboards', through='KeyboardButtonsOrdering',
                                     verbose_name=_('Buttons'))

    class Meta:
        verbose_name = _('Keyboard')
        verbose_name_plural = _('Keyboards')


class KeyboardButtonsOrdering(models.Model):
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE, related_name='buttons_ordering',
                                 verbose_name=_('Keyboard'))
    button = models.ForeignKey(Button, on_delete=models.CASCADE, related_name='ordering', verbose_name=_('Keyboard'))
    ordering = models.PositiveIntegerField(verbose_name='Ordering')

    class Meta:
        verbose_name = _('Keyboard buttons ordering')
        verbose_name_plural = _('Keyboard buttons orderings')


class Message(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name=_('Code'))
    text = models.TextField()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.code


class TelegramUser(models.Model):
    id = models.IntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Username'))
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Full name'))
    phone_number = models.CharField(max_length=20, null=True, verbose_name=_('Phone number'))
    email = models.CharField(max_length=200, null=True, verbose_name=_('Email'))
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, null=True, verbose_name=_('Language'))

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        ret = self.full_name if self.full_name else str(self.id)
        return ret
