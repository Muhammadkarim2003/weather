WEATHER_TRANSLATIONS = {
    "clear sky": "Musaffo osmon",
    "few clouds": "Kam bulutli",
    "scattered clouds": "Tarqalgan bulutlar",
    "broken clouds": "Parcha bulutlar",
    "overcast clouds": "To‘liq bulutli",
    "light rain": "Yengil yomg‘ir",
    "moderate rain": "O‘rtacha yomg‘ir",
    "heavy intensity rain": "Kuchli yomg‘ir",
    "thunderstorm": "Momaqaldiroq",
    "snow": "Qor",
    "mist": "Tuman",
    "haze": "Xira havo",
    "smoke": "Tutun",
    "dust": "Chang",
    "fog": "Tumanlik",
    "sand": "Qum bo‘roni",
}

def translate_description(description):
    return WEATHER_TRANSLATIONS.get(description.lower(), description)




def get_uzbek_weekday(weekday_en):
    weekdays = {
        'Monday': 'Dushanba',
        'Tuesday': 'Seshanba',
        'Wednesday': 'Chorshanba',
        'Thursday': 'Payshanba',
        'Friday': 'Juma',
        'Saturday': 'Shanba',
        'Sunday': 'Yakshanba',
    }
    return weekdays.get(weekday_en, weekday_en)
