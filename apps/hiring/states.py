from aiogram.dispatcher.filters.state import StatesGroup, State


class HiringForm(StatesGroup):
    categories = State()
    resume_filling = State()
    resume_select = State()


prev_resume_states = {
            'photo': 'email',
            'instagram': 'photo',
            'education': 'instagram',
            'work_experience': 'education',
            'skills': 'work_experience',
            'languages': 'skills',
            'driver_license': 'languages',
            'ready_for_business_trips': 'driver_license',
            'additional_info': 'ready_for_business_trips'
        }