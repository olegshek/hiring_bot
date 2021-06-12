from core.filters import message_filter


def select_category(query):
    return 'category' in query.data


async def yes_or_no(message):
    return await message_filter(message, 'yes_or_no')


def is_switch(query):
    data = query.data.split(';')
    return len(data) == 2 and data[1] in ['gte', 'lte']


def is_send_request(query):
    return 'send_request' in query.data
