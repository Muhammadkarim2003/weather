from django.shortcuts import render
from decouple import config
import requests
from .utils import translate_description, get_uzbek_weekday
from datetime import datetime
from django.http import HttpResponse

from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4


API_KEY = config('OPENWEATHER_API_KEY')

def home(request):
    weather_data = {}

    if request.method == 'POST':
        city = request.POST.get('city')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            description_en = data['weather'][0]['description']
            description_uz = translate_description(description_en)

            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': description_uz,
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'icon': data['weather'][0]['icon'],
            }
            
        else:
            weather_data = {'error': 'Shahar topilmadi. Iltimos, boshqa shahar kiriting.'}

    return render(request, 'weather/home.html', {'weather_data': weather_data})

def forecast(request):
    city = request.GET.get('city')
    forecast = []

    if city:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            seen_dates = set()

            for item in data['list']:
                date_txt = item['dt_txt'].split()[0]  # Faqat YYYY-MM-DD qismi
                if date_txt not in seen_dates:
                    seen_dates.add(date_txt)
                    date_obj = datetime.strptime(date_txt, "%Y-%m-%d")
                    weekday_en = date_obj.strftime("%A")
                    weekday_uz = get_uzbek_weekday(weekday_en)
                    formatted_date = f"{weekday_uz}, {date_obj.strftime('%d-%b')}"

                    forecast.append({
                        'date': formatted_date,
                        'temp': item['main']['temp'],
                        'description': translate_description(item['weather'][0]['description']),
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed'],
                        'icon': item['weather'][0]['icon']
                    })

                    if len(forecast) == 7:
                        break

    return render(request, 'weather/forecast.html', {'forecast': forecast, 'city': city})


# def weekly_forecast(request):
#     city = request.GET.get('city')
#     forecast_data = []
#     if city:
#         url = f'https://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt=7&appid={API_KEY}&units=metric'
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             for day in data['list']:
#                 forecast_data.append({
#                     'date': datetime.fromtimestamp(day['dt']).strftime('%d-%m-%Y'),
#                     'temperature': day['temp']['day'],
#                     'description': translate_description(day['weather'][0]['description']),
#                     'icon': day['weather'][0]['icon']
#                 })

#     return render(request, 'weather/weekly.html', {
#         'forecast_data': forecast_data,
#         'city': city
#     })
    
    
    
def download_forecast_pdf(request):
    city = request.GET.get('city')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{city}_7_kunlik_ob_havo.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"{city} uchun 7 kunlik ob-havo ma'lumotlari")

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    api_response = requests.get(url)

    if api_response.status_code == 200:
        data = api_response.json()
        daily_data = {}
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in daily_data:
                daily_data[date] = {
                    'temp': item['main']['temp'],
                    'description': translate_description(item['weather'][0]['description']),
                }
            if len(daily_data) == 7:
                break

        y = 760
        for date, info in daily_data.items():
            p.drawString(80, y, f"{date} — {info['temp']}°C — {info['description']}")
            y -= 30

    else:
        p.drawString(100, 750, "Ma'lumot olishda xatolik yuz berdi.")

    p.showPage()
    p.save()
    return response

