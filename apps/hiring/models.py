from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.bot.models import TelegramUser


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(verbose_name=_('File'))

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')


class Resume(models.Model):
    resume_id = models.IntegerField(null=True, verbose_name=_('Resume id'))
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='resumes', verbose_name=_('User'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='resumes', verbose_name=_('Category'))

    instagram = models.CharField(max_length=200, null=True, verbose_name=_('Instagram'))
    education = models.TextField(null=True, verbose_name=_('Education'))
    work_experience = models.TextField(null=True, verbose_name=_('Work experience'))
    skills = models.TextField(null=True, verbose_name=_('Skills'))
    languages = models.TextField(null=True, verbose_name=_('Languages'))
    driver_license = models.BooleanField(null=True, verbose_name=_('Driver license'))
    ready_for_business_trips = models.BooleanField(null=True, verbose_name=_('Ready for business trips'))
    additional_info = models.TextField(null=True, verbose_name=_('Additional info'))

    photo = models.ImageField(null=True, verbose_name=_('Photo'))

    filled_out_at = models.DateTimeField(null=True, verbose_name=_('Filled out at'))
    approved = models.BooleanField(default=False, verbose_name=_('Approved'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created at'))

    class Meta:
        ordering = ('-filled_out_at',)
        verbose_name = _('Resume')
        verbose_name_plural = _('Resumes')

    def __str__(self):
        return f'{self.resume_id} - {self.category.name}'

    @property
    def phone_number(self):
        return self.user.phone_number

    @property
    def email(self):
        return self.user.email


class HiringRequest(models.Model):
    request_id = models.IntegerField(null=True, verbose_name=_('Request id'))
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='hiring_requests',
                             verbose_name=_('User'))
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='hiring_requests',
                               verbose_name=_('Resume'))
    message_id = models.IntegerField(null=True, verbose_name=_('Message id'))

    approved = models.BooleanField(default=False, verbose_name=_('Approved'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created at'))

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Hiring request')
        verbose_name_plural = _('Hiring requests')

    def __str__(self):
        return str(self.resume_id)
