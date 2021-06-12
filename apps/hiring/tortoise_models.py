from django.utils import timezone
from tortoise import models, fields

from core.utils import generate_number


class Category(models.Model):
    name_ru = fields.CharField(max_length=200)
    name_en = fields.CharField(max_length=200)

    class Meta:
        table = 'hiring_category'


class File(models.Model):
    file = fields.TextField()

    class Meta:
        table = 'hiring_file'


class Resume(models.Model):
    resume_id = fields.IntField(default=generate_number)
    user = fields.ForeignKeyField('bot.TelegramUser', on_delete=fields.CASCADE, related_name='resumes')
    category = fields.ForeignKeyField('hiring.Category', on_delete=fields.CASCADE, related_name='resumes')

    instagram = fields.CharField(null=True, max_length=200)
    education = fields.TextField(null=True)
    work_experience = fields.TextField(null=True)
    skills = fields.TextField(null=True)
    languages = fields.TextField(null=True)
    driver_license = fields.BooleanField(null=True)
    ready_for_business_trips = fields.BooleanField(null=True)
    additional_info = fields.TextField(null=True)

    photo = fields.TextField(null=True)

    filled_out_at = fields.DatetimeField(null=True)
    approved = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(default=timezone.now)

    class Meta:
        table = 'hiring_resume'


class HiringRequest(models.Model):
    request_id = fields.IntField(default=generate_number)
    user = fields.ForeignKeyField('bot.TelegramUser', on_delete=fields.CASCADE, related_name='hiring_requests')
    resume = fields.ForeignKeyField('hiring.Resume', on_delete=fields.CASCADE, related_name='hiring_requests')
    message_id = fields.IntField(null=True)

    approved = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(default=timezone.now)

    class Meta:
        table = 'hiring_hiringrequest'
