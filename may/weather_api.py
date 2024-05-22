import requests
import json

import os

def call_current_weather(city = 'Seoul'):
    api_key = os.environ.get('WEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&lang=kr&units=metric'
    result = requests.get(url)
    
    if result.status_code == 200:
        
        data = json.loads(result.text)
        # 필요한 정보들
        loc = data['name']
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        weather = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        # rain = data['rain']['rain.3h']
        
        # return f'현재 {loc} 의 날씨는 {weather} 이며, 최고기온은 {temp_max}, 최저기온은 {temp_min}입니다.\n평균기온은 {temp}이며, 습도 {humidity}, 풍속 {wind_speed}입니다.' 
        weather_info = {
        "location": loc,
        "weather": weather,
        "temp_max": temp_max,
        "temp_min": temp_min,
        "temp": temp,
        "humidity": humidity,
        "wind_speed": wind_speed}
        
        return weather_info    
    else:    
        return 'Unable to retrieve weather information.'