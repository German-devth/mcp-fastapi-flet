import logging
from typing import Any, Dict

import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city: str) -> Dict[str, Any]:
    """
    Получает данные о погоде для заданного города
    Args:
         city:
            Название города в виде строки
    Returns:
         Словарь с информацией о погоде
    """
    logging.info(f"Received request for weather: {city}")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "description": weather_data["weather"][0]["description"]
    }
