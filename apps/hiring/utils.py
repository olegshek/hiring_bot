from django.conf import settings

from apps.bot import messages, bot


async def send_resume_to_channel(resume):
    resume_user = await resume.user
    message = f'<b>ID</b>: {resume.resume_id}\n'
    message += (await messages.get_message('resume_info', 'ru')) % {
        'full_name': resume_user.full_name,
        'education': resume.education,
        'work_experience': resume.work_experience,
        'skills': resume.skills,
        'languages': resume.languages,
        'driver_license': '✅' if resume.driver_license else '❌',
        'ready_for_business_trips': '✅' if resume.ready_for_business_trips else '❌',
        'additional_info': resume.additional_info
    }
    channel_id = settings.RESUMES_CHANNEL_ID

    if len(message) > 4096:
        for i in range(0, len(message), 4096):
            await bot.send_message(channel_id, message[i:i + 4096], parse_mode='HTML')
    else:
        await bot.send_message(channel_id, message, parse_mode='HTML')


async def send_candidate_request_to_channel(request):
    resume = await request.resume
    request_user = await request.user
    message = f'<b>ID</b>: {request.request_id}\n' \
              f'<b>От пользователя</b>: {request_user.full_name}\n' \
              f'<b>ID резюме</b>: {resume.resume_id}'
    await bot.send_message(settings.CANDIDATE_REQUESTS_CHANNEL_ID, message, parse_mode='HTML')
