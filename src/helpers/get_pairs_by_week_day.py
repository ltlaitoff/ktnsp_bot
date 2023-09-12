import pandas
from helpers.check_lesson_on_week_not_compatibility import check_lesson_on_week_not_compatibility
from config import lesson_times
from helpers.get_todays_schedule_iterrows import get_todays_schedule_iterrows


def getText(text, var, type="default"):
    if (pandas.isna(var)):
        return ""

    varText = var if type != "link" else f'<a href="{var}">link</a>'

    return f"{text}: {varText}\n"


def get_pairs_by_week_day(week_day, next=False, detailed=False):
    todays_schedule = get_todays_schedule_iterrows(week_day)
    text = []

    for _, row in todays_schedule:
        type_lesson = row['type_lesson']
        period = row['period']
        time_start, time_end = lesson_times[period - 1]
        subject = row['subject']

        if pandas.isna(type_lesson):
            continue

        if (check_lesson_on_week_not_compatibility(
            row['type'],
            subject,
            next
        )):
            continue

        "🐤🐧🐦"

        if (type_lesson == "ЛК"):
            smile_type = "🐦"
        elif (type_lesson == "ЛБ"):
            smile_type = "🐤"
        elif (type_lesson == "ПР"):
            smile_type = "🐧"
        else:
            smile_type = "🐔"

        smile = "🧖🏿‍♀️" if subject == 'Л-МВ' else "🧖🏻‍♀️" if subject == 'ВТтаВД' else ""

        if (detailed == True):
            teacher = row['teacher']
            meeting_link = row['meeting_link']
            zoom_code = row['zoom_code']
            zoom_password = row['zoom_password']
            link_to_platform = row['link_to_platform']
            email = row['email']
            telegram = row['telegram']
            additional_text = row['additional_text']

            text.append(f"<b>Pair {period}</b> | ⏳ {time_start} - {time_end}:\n" +
                        f"🔔 Subject: {smile_type} {type_lesson} {smile} {subject}\n" +
                        getText("👨‍🏫 Teacher", teacher) +
                        getText("🔗 Meeting", meeting_link, "link") +
                        getText("🆔 Zoom code", zoom_password) +
                        getText("🔐 Zoom password", zoom_code) +
                        getText("🌵 Platform", link_to_platform, "link") +
                        getText("📧 Email", email) +
                        getText("📞 Telegram", telegram) +
                        getText("🤘🏿 Additional", additional_text)
                        )

        else:
            text.append(
                f'{period} | {time_start} - {time_end}: {smile_type}{type_lesson} {smile}{subject}')

    if (len(text) == 0):
        return "Пар немає\n"

    if (detailed):
        return "----\n".join(text)

    return "\n".join(text)
