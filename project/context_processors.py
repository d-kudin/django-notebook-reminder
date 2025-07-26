# project/context_processors.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def weather_context(request):
    api_key = os.getenv('WEATHER_API_KEY', 'demo_key')
    city = 'Warsaw'
    weather = {
        'temperature': 'N/A',
        'description': 'N/A',
        'city': 'N/A'
    }
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pl&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'city': data['name']
            }
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
    
    return {'weather': weather}