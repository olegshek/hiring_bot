from uuid import uuid4

from aiogram.types import ContentType, Message
from django.utils import timezone

from apps.bot import bot, keyboards, dispatcher as dp, messages
from apps.bot.callback_filters import message_is_not_back, message_is_not_command
from apps.bot.keyboards import resume_menu
from apps.bot.telegram_views.bot import send_main_menu
from apps.bot.tortoise_models import TelegramUser, Button
from apps.bot.utils import try_delete_message
from apps.hiring import callback_filters
from apps.hiring.states import HiringForm
from apps.hiring.tortoise_models import Category, Resume, HiringRequest
from apps.hiring.utils import send_resume_to_channel, send_candidate_request_to_channel


async def send_categories(user_id, locale, message_id=None):
    categories = await Category.all().order_by(f'name_{locale}')
    if categories:
        await HiringForm.categories.set()

        if message_id:
            await try_delete_message(user_id, message_id)

        await bot.send_message(
            user_id,
            await messages.get_message('categories', locale),
            reply_markup=await keyboards.categories(categories, locale)
        )


async def send_resume_input(user_id, locale, message_code, state):
    async with state.proxy() as data:
        data['resume_state'] = message_code

    keyboard = keyboards.back_keyboard(locale)

    if message_code in ['driver_license', 'ready_for_business_trips']:
        keyboard = keyboards.yes_or_no(locale)

    await bot.send_message(
        user_id,
        await messages.get_message(message_code, locale),
        reply_markup=await keyboard
    )


async def fill_out_resume(resume, locale, state, message_id=None):
    user_id = resume.user_id
    await HiringForm.resume_filling.set()

    if message_id:
        await try_delete_message(user_id, message_id)

    if not (await resume.user).email:
        return await send_resume_input(user_id, locale, 'email', state)

    if not resume.photo:
        return await send_resume_input(user_id, locale, 'photo', state)

    if not resume.instagram:
        return await send_resume_input(user_id, locale, 'instagram', state)

    if not resume.education:
        return await send_resume_input(user_id, locale, 'education', state)

    if not resume.work_experience:
        return await send_resume_input(user_id, locale, 'work_experience', state)

    if not resume.skills:
        return await send_resume_input(user_id, locale, 'skills', state)

    if not resume.languages:
        return await send_resume_input(user_id, locale, 'languages', state)

    if resume.driver_license is None:
        return await send_resume_input(user_id, locale, 'driver_license', state)

    if resume.ready_for_business_trips is None:
        return await send_resume_input(user_id, locale, 'ready_for_business_trips', state)

    if not resume.additional_info:
        return await send_resume_input(user_id, locale, 'additional_info', state)

    resume.filled_out_at = timezone.now()
    await resume.save()
    await send_resume_to_channel(resume)

    telegram_user = await TelegramUser.get(id=user_id)
    text = (await messages.get_message('request_accepted', locale))
    text += f' {resume.resume_id}'
    await bot.send_message(user_id, text, reply_markup=keyboards.remove_keyboard)

    await send_main_menu(telegram_user, locale, state)


async def send_resume_menu(user_id, message_id, locale, state, resume_id=None, option=None):
    async with state.proxy() as data:
        category_id = data['category_id']

    requested_resumes = await HiringRequest.filter(user_id=user_id).values_list('resume_id', flat=True)

    exclude_data = {'id__in': requested_resumes}
    filter_data = {
        'category_id': category_id,
        'approved': True
    }
    order_by = '-created_at'

    if resume_id and option:
        checked_resume = await Resume.get(id=resume_id)
        exclude_data['id'] = resume_id
        filter_data[f'created_at__{option}'] = checked_resume.created_at
        if option == 'gte':
            order_by = 'created_at'

    resume = await Resume.filter(**filter_data). \
        exclude(**exclude_data). \
        order_by(order_by). \
        first()

    if not resume:
        return

    resume_ids = await Resume.filter(category_id=category_id, approved=True). \
        exclude(id__in=requested_resumes). \
        order_by('-created_at'). \
        values_list('id', flat=True)
    resume_number = resume_ids.index(resume.id) + 1
    resumes_quantity = len(resume_ids)

    await try_delete_message(user_id, message_id)

    resume_user = await resume.user
    message = (await messages.get_message('resume_info', locale)) % {
        'full_name': resume_user.full_name,
        'education': resume.education,
        'work_experience': resume.work_experience,
        'skills': resume.skills,
        'languages': resume.languages,
        'driver_license': '✅' if resume.driver_license else '❌',
        'ready_for_business_trips': '✅' if resume.ready_for_business_trips else '❌',
        'additional_info': resume.additional_info
    }

    await HiringForm.resume_select.set()

    keyboard = await resume_menu(resume.id, locale, resumes_quantity, resume_number)

    with open(f'media/{resume.photo}', 'rb') as photo:
        await bot.send_photo(user_id, photo)

    if len(message) > 4096:
        elements_qnt = len(message) // 4096

        for i, x in enumerate(range(0, len(message), 4096)):
            if i + 1 <= elements_qnt:
                reply_keyboard = None
            else:
                reply_keyboard = keyboard

            await bot.send_message(user_id, message[x:x + 4096], reply_markup=reply_keyboard, parse_mode='HTML')
    else:
        await bot.send_message(user_id, message, reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query_handler(callback_filters.select_category, state=HiringForm.categories.state)
async def select_category(query, locale, state):
    user_id = query.from_user.id
    message_id = query.message.message_id
    category_id = int(query.data.split(':')[1])

    async with state.proxy() as data:
        hiring_type = data['hiring_type']
        data['category_id'] = category_id

    if hiring_type == 'submit_resume':
        await Resume.filter(filled_out_at__isnull=True).delete()

        if await Resume.filter(category_id=category_id):
            await bot.send_message(user_id, await messages.get_message('resume_exist', locale))
            return await send_categories(user_id, locale, message_id)

        resume = await Resume.create(user_id=user_id, category_id=category_id)

        async with state.proxy() as data:
            data['resume_id'] = resume.id

        await fill_out_resume(resume, locale, state, message_id)

    if hiring_type == 'find_candidate':
        await send_resume_menu(user_id, message_id, locale, state)


@dp.message_handler(message_is_not_back, message_is_not_command, state=HiringForm.resume_filling.state,
                    content_types=[ContentType.TEXT])
async def apply_resume_data(message, locale, state):
    async with state.proxy() as data:
        resume_id = data['resume_id']
        resume_state = data['resume_state']

    resume = await Resume.get(id=resume_id)

    if resume_state == 'photo':
        return await fill_out_resume(resume, locale, state)

    if resume_state in ['driver_license', 'ready_for_business_trips'] and not await callback_filters.yes_or_no(message):
        return await fill_out_resume(resume, locale, state)

    resume_data = message.text

    if resume_state in ['driver_license', 'ready_for_business_trips']:
        yes_or_no_button_code = (await Button.filter(**{f'text_{locale}': message.text}).first()).code
        resume_data = True if yes_or_no_button_code == 'yes' else False

    if resume_state == 'email':
        user = await resume.user
        setattr(user, resume_state, resume_data)
        await user.save()
    else:
        setattr(resume, resume_state, resume_data)
        await resume.save()

    await fill_out_resume(resume, locale, state)


@dp.message_handler(content_types=[ContentType.PHOTO, ContentType.DOCUMENT], state=HiringForm.resume_filling.state)
async def apply_resume_photo(message: Message, locale, state):
    async with state.proxy() as data:
        resume_id = data['resume_id']

    resume = await Resume.get(id=resume_id)

    if not message.photo and not message.document:
        return await fill_out_resume(resume, locale, state)

    photo = message.photo[-1] if message.photo else message.document
    photo_name = f'{uuid4()}.jpg'
    await photo.download(f'media/{photo_name}', make_dirs=True)

    resume.photo = photo_name
    await resume.save()

    await fill_out_resume(resume, locale, state)


@dp.callback_query_handler(callback_filters.is_switch, state=HiringForm.resume_select.state)
async def switch_resume(query, state, locale):
    user_id = query.from_user.id
    data = query.data.split(';')
    resume_id = int(data[0])
    lookups = data[1]

    await send_resume_menu(user_id, query.message.message_id, locale, state, resume_id, lookups)


@dp.callback_query_handler(callback_filters.is_send_request, state=HiringForm.resume_select.state)
async def send_hiring_request(query, state, locale):
    user_id = query.from_user.id
    data = query.data.split(';')
    resume_id = int(data[1])

    hiring_request = await HiringRequest.create(resume_id=resume_id, user_id=user_id)
    await send_candidate_request_to_channel(hiring_request)
    telegram_user = await TelegramUser.get(id=user_id)

    await try_delete_message(user_id, query.message.message_id)
    text = (await messages.get_message('request_accepted', locale))
    text += f' {hiring_request.request_id}'
    message = await bot.send_message(user_id, text, reply_markup=keyboards.remove_keyboard)

    hiring_request.message_id = message.message_id
    await hiring_request.save()

    await send_main_menu(telegram_user, locale, state)
