import pandas


def get_lesson_message(
    time_start,
    time_end,
    subject,
    teacher,
    type_lesson,
    additional_text,
    meeting_link,
    zoom_code,
    zoom_password,
    email,
    telegram,
):
    text = (
        f'Наступна пара: "<code>{subject}</code>"\n'
        f'Викладач: <code>{teacher}</code>\n'
        f'Час: {time_start} - {time_end}\n'
    )

    if not pandas.isna(type_lesson) and type_lesson != "Null":
        text += f'Тип пари: "<code>{type_lesson}</code>"\n'

    if not pandas.isna(additional_text) and additional_text != "Null":
        text += f'Додадкова інфа: "<code>{additional_text}</code>"\n'

    if not pandas.isna(meeting_link) and meeting_link != "Null":
        text += f'<a href="{meeting_link}">Посилання на зустріч</a>\n'

    if not pandas.isna(zoom_code) and zoom_code != "Null":
        text += f'Ідентифікатор Zoom: {zoom_code}\n'

    if not pandas.isna(zoom_password) and zoom_password != "Null":
        text += f'Пароль Zoom: {zoom_password}\n'

    if not pandas.isna(email) and email != "Null":
        text += f'Електронна адреса: {email}\n'

    if not pandas.isna(telegram) and telegram != "Null":
        text += f'Telegram: {telegram}\n'

    return text
