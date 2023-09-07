from helpers.get_lesson_message import get_lesson_message


def get_lesson_message_by_lesson(
    time_start,
    time_end,
    lesson
):
    return get_lesson_message(
        time_start,
        time_end,
        lesson['subject'],
        lesson['teacher'],
        lesson['type_lesson'],
        lesson['additional_text'],
        lesson['meeting_link'],
        lesson['zoom_code'],
        lesson['zoom_password'],
        lesson['email'],
        lesson['telegram'],
    )
