
import pandas
from config import data


def getText(text, var, type="default"):
    if (pandas.isna(var)):
        return ""

    varText = var if type != "link" else f'<a href="{var}">link</a>'

    return f"{text}: {varText}\n"


def get_all_controller():
    allData = data.iterrows()
    text = []

    for _, row in allData:
        day_of_the_week = row['day_of_the_week']
        period = row['period']
        type_lesson = row['type_lesson']
        subject = row['subject']
        teacher = row['teacher']
        meeting_link = row['meeting_link']
        zoom_code = row['zoom_code']
        zoom_password = row['zoom_password']
        link_to_platform = row['link_to_platform']
        email = row['email']
        telegram = row['telegram']
        additional_text = row['additional_text']
        type = row['type']

        type = 'Знаменник' if True else 'Чисельник'

        text.append(f"🔔 Subject: {type_lesson} {subject}\n" +
                    getText("👨‍🏫 Teacher", teacher) +
                    getText("🔗 Meeting", meeting_link, "link") +
                    getText("🌵 Platform", link_to_platform, "link") +
                    getText("📧 Email", email) +
                    getText("📞 Telegram", telegram) +
                    getText("🤘🏿 Additional", additional_text)
                    )

    return "-------\n".join(text)
