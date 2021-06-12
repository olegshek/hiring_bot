from django.conf import settings
from django.dispatch import Signal, receiver
from telebot import TeleBot

from apps.bot.models import Message
from apps.hiring.models import HiringRequest

hiring_request_approved = Signal(providing_args=['sender', 'instance'])

bot = TeleBot(token=settings.TELEGRAM_TOKEN)


@receiver(hiring_request_approved, sender=HiringRequest)
def send_resume_contacts(sender, instance, *args, **kwargs):
    locale = instance.user.language
    text = getattr(Message.objects.get(code='resume_contacts'), f'text_{locale}') % {
        'full_name': instance.resume.user.full_name,
        'category': getattr(instance.resume.category, f'name_{locale}'),
        'phone_number': instance.resume.phone_number,
        'email': instance.resume.email,
        'instagram': instance.resume.instagram
    }
    bot.send_message(instance.user.id, text, reply_to_message_id=instance.message_id if instance.message_id else None,
                     parse_mode='HTML')
