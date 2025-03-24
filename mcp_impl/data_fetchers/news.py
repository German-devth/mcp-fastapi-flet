import os
from typing import List

import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(city: str) -> List[str]:
    """
    Получает заголовки новостей для заданного города
    Args:
        city:
            Название города в виде строки
    Returns:
        Список заголовков новостей в виде строк
    """
    date_from: str = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url: str = f"https://newsapi.org/v2/everything?q={city}&from={date_from}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()

    titles: List[str] = [
        article.get("title")
        for article in news_data.get("articles", [])
        if article.get("title")
    ]
    return titles
